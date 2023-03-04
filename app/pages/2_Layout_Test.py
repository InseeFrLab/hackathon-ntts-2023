import streamlit as st
from streamlit_utils import read_csv, read_html, add_logos
import plotly.express as px


st.set_page_config(page_title="Layout test")

add_logos()

st.markdown("# Layout test")
st.sidebar.header("Layout test")


tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")


###
# Display data
###
df_users = read_csv("projet-hackathon-ntts-2023/data/kaggle_user_data.csv")

st.subheader('Raw user data :')
st.write(df_users)

st.subheader('Raw user data :')
st.write(df_users)

###
# Plotly example
###
df_merchants = read_csv(
    "projet-hackathon-ntts-2023/data/MerchantHierarchyMaster.csv"
)

# Obtenir le nombre d'occurrences de chaque secteur
sectors_count = df_merchants['Sector'].value_counts().reset_index()

# Renommer les colonnes pour plus de clarté
sectors_count.columns = ['Sector', 'Count']

# Calculer la fréquence de chaque secteur
total_count = sectors_count['Count'].sum()
sectors_count['Frequency'] = sectors_count['Count'] / total_count

# Identifier les secteurs avec une fréquence inférieure à 5%
other_sectors = sectors_count.loc[
    sectors_count['Frequency'] < 0.05, 'Sector'
].tolist()

# Mettre à jour le DataFrame en remplaçant les noms
# des secteurs avec une fréquence inférieure à 1%
sectors_count.loc[
    sectors_count['Sector'].isin(other_sectors), 'Sector'
] = 'Autre'
sectors_count = sectors_count.groupby('Sector')['Count'].sum().reset_index()

# Créer le graphique camembert
fig = px.pie(sectors_count, values='Count', names='Sector',
             title='Répartition des secteurs parmi les merchants')

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

html_leaflet = read_html(
    "projet-hackathon-ntts-2023/plots/carte_test.html"
)
st.components.v1.html(html_leaflet)
