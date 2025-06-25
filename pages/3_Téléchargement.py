import streamlit as st
import os

st.set_page_config(page_title="Téléchargement des données brutes", layout="centered", page_icon="📥")
st.title("📥 Téléchargement des données brutes Web Scraper")

# Dictionnaire des fichiers à télécharger
FILES = {
    "Appartements": "data/raw/appartements_coinafrique_WSc.csv",
    "Villas": "data/raw/Villas_coinafrique_WSc.csv",
    "Terrains": "data/raw/terrains_coinafrique_WSc.csv"
}

# Affichage des boutons de téléchargement
for label, path in FILES.items():
    if os.path.exists(path):
        with open(path, "rb") as f:
            st.download_button(
                label=f"Télécharger {label}",
                data=f,
                file_name=os.path.basename(path),
                mime="text/csv",
                key=label  # clé unique pour chaque bouton
            )
    else:
        st.warning(f"❌ Le fichier pour {label} n'est pas disponible.")

st.info("Les fichiers contiennent les données brutes issues du scraping via Web Scraper.")
