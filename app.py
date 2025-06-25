import os
os.environ["STREAMLIT_SERVER_ENABLE_STATIC_FILE_WATCHER"] = "false"
import streamlit as st

# Configuration générale de la page
st.set_page_config(
    page_title="🌐 Web Scraper App",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bannière avec titre et description
st.markdown(
    """
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #0E1117;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    <div class="block-container">
        <p class="main-title">🕸️ Web Scraper App</p>
        <p class="subtitle">Explorez, collectez et analysez facilement les données du web</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Affiche image en haut
st.image(
    "https://img.freepik.com/free-vector/web-scraping-concept-illustration_114360-9334.jpg",
    use_container_width=True, 
    caption="Illustration du scraping web"
)
# Section d'accueil
st.markdown("## 🚀 Fonctionnalités de l'application")
st.markdown("""
- 📄 **Scraper** des données depuis des sites web
- 📊 **Analyser** les données via des dashboards interactifs
- 📝 **Évaluer** l'application via un formulaire simple
- 💾 **Télécharger** les données brutes

Utilisez le menu à gauche pour commencer 👈
""")

# Sidebar
st.sidebar.header("📂 Navigation")
st.sidebar.success("➡️ Sélectionnez une page dans le menu")

st.sidebar.markdown("---")
st.sidebar.markdown("👤 Réalisé par **Marième FAYE**")
