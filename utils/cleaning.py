# utils/cleaning.py
import pandas as pd
import re

def clean_data(df):
    # Nettoyage des prix
    df['prix'] = df['prix'].apply(lambda x: float(re.sub(r'[^\d.,]', '', x).replace(',', '.')))
    
    # Conversion des notes
    df['note'] = pd.to_numeric(df['note'], errors='coerce')
    
    # Suppression des doublons
    df = df.drop_duplicates(subset='nom')
    
    # Filtrage des valeurs aberrantes
    df = df[(df['prix'] > 0) & (df['prix'] < 1000)]
    
    return df