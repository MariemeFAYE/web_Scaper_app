import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from utils.scraping import scrape_site  # Fonction personnalisée

st.title("🔍 Scraping de données")

# Configuration du scraping
base_url = st.text_input("URL de base")
pages = st.number_input("Nombre de pages", 1, 100, 5)
scrape_button = st.button("Lancer le scraping")

if scrape_button:
    progress_bar = st.progress(0)
    scraped_data = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        data = scrape_site(url)  # À implémenter dans utils/scraping.py
        scraped_data.extend(data)
        progress_bar.progress(page / pages)
    
    df = pd.DataFrame(scraped_data)
    raw_path = "data/raw/scraped_data.csv"
    df.to_csv(raw_path, index=False)
    st.success(f"Données sauvegardées dans {raw_path}")