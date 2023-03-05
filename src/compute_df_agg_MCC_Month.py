### Preparing packages and spark config

# loading necessary libraries
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, FloatType
import pyspark.sql.functions as F
import os
import json
import netifaces as ni

# importing the AWS credentials from the json file
f = open("/home/jovyan/temporary_creds.json")
creds=json.load(f)
f.close()

# adding the AWS credentials to environment variables
os.environ['AWS_ACCESS_KEY_ID'] = creds['Credentials']['AccessKeyId']
os.environ['AWS_SECRET_ACCESS_KEY'] = creds['Credentials']['SecretAccessKey']
os.environ['AWS_SESSION_TOKEN'] = creds['Credentials']['SessionToken']
os.environ['AWS_DEFAULT_REGION']="eu-west-1"

# setting config values for spark and postgres 
dsl_name="NSI-FR"  # e.g. "ESTAT-ADMINS"
spark_master="spark://spark-1677874290-master-0.spark-1677874290-headless.nsi-fr.svc.cluster.local:7077"
#spark_master="spark://spark-1677788907-master-0.spark-1677788907-headless.nsi-fr.svc.cluster.local:7077" # e.g. "spark://spark-1677618294-master-0.spark-1677618294-headless.estat-admins.svc.cluster.local:7077"
ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
spark_driver_host=ip.replace(".","-")+"."+dsl_name.lower()+".pod.cluster.local"

# Spark session for a large service configuration
spark = SparkSession.builder \
                    .master(spark_master) \
                    .config("spark.submit.deployMode", "client") \
                    .config("spark.driver.host",spark_driver_host) \
                    .config("spark.executor.memory","13000m") \
                    .config("spark.driver.memory","13000m") \
                    .config("spark.driver.cores","1") \
                    .config("spark.driver.port", "9000")\
                    .config("spark.jars.packages","org.postgresql:postgresql:42.5.0,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-pom:1.11.901,org.apache.hadoop:hadoop-common:3.3.1,org.apache.hadoop:hadoop-client:3.3.1,com.amazonaws:aws-java-sdk:1.11.901,org.apache.spark:spark-hadoop-cloud_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.1")\
                    .getOrCreate()

spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.environ.get('AWS_ACCESS_KEY_ID'))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.environ.get('AWS_SECRET_ACCESS_KEY'))
# spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.session.token", os.environ.get('AWS_SESSION_TOKEN'))
# spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint.region", os.environ.get('AWS_DEFAULT_REGION'))
# spark.sparkContext._jsc.hadoopConfiguration().set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")

### Load data from the s3 bucket

df = spark.read.parquet("s3a://ecdataplatform-nsi-fr-results-bucket/data_pannel.parquet")

df = df.filter(F.substring(F.col('TxnDate'), 1, 4) > "2017")
df = df.filter(F.substring(F.col('TxnDate'), 1, 7) < "2023-02")

df = df.withColumn('TxnMonth', F.substring(F.col('TxnDate'), 1, 7))

df_agg = (df
      .groupby('MCC', 'TxnMonth')
      .agg(
          F.sum("Amount").alias("Amount"),
          F.count("TxnDate").alias("Nb_Txn")
      )
     )

df_agg.write.mode("overwrite").parquet("s3a://ecdataplatform-nsi-fr-results-bucket/data_agg_MCC_Month.parquet")