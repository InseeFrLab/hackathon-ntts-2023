#!/bin/bash

pip install -r app/requirements.txt

AWS_ACCESS_KEY_ID=`vault kv get -field=ACCESS_KEY onyxia-kv/projet-hackathon-ntts-2023/env` && export AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=`vault kv get -field=SECRET_KEY onyxia-kv/projet-hackathon-ntts-2023/env` && export AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
export MC_HOST_s3=https://$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY@$AWS_S3_ENDPOINT

streamlit run app/🇫🇷4C_Home_page.py
