import streamlit as st

# Configuration générale
st.set_page_config(
    page_title="Accueil | Web Scraper App",
    layout="wide",
    page_icon="https://your-domain.com/favicon.png" 
)

# Bannière personnalisée
st.image("https://your-custom-banner-url.com/banner.png", use_container_width=True) 

# Titre principal centré avec style
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #2E86C1;'>Bienvenue sur <span style="color: #117864;">Web Scraper App</span></h1>
        <p style='font-size: 20px;'>Extraire, visualiser et analyser les données web n’a jamais été aussi simple !</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Présentation des fonctionnalités
st.subheader("🚀 Fonctionnalités clés de l’application")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🕸️ Scraping de données")
    st.write("- Extraction automatisée depuis plusieurs pages web")
    st.write("- Utilisation de **BeautifulSoup** et **Web Scraper**")

    st.markdown("### 📊 Analyse visuelle")
    st.write("- Dashboards interactifs avec **Plotly** et **Matplotlib**")
    

with col2:
    st.markdown("### 📥 Téléchargement facile")
    st.write("- Exporte les données brutes en `.csv`")

    st.markdown("### 📝 Feedback utilisateur")
    st.write("- Formulaire d’évaluation intégré")

st.markdown("---")

# Appel à action / navigation
st.info("📂 Utilisez le menu à gauche pour naviguer dans les différentes pages de l’application.")
