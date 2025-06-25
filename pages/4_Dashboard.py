import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os

# Configuration de la page
st.set_page_config(page_title="Dashboard CoinAfrique", layout="wide", page_icon="📊")
st.title("📊 Tableau de bord interactif des biens immobiliers CoinAfrique")

# Liste des fichiers disponibles
DATASETS = {
    "Appartements": "data/cleaned/appartement_coinafrique_bs.csv",
    "Villas": "data/cleaned/villas_coinafrique_bs.csv",
    "Terrains": "data/cleaned/terrains_coinafrique_bs.csv"
}

# Chargement des données
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# 🔧 Nettoyage des colonnes numériques
def clean_price_column(df):
    df["Prix"] = pd.to_numeric(df["Prix"], errors="coerce")
    return df

def clean_nombre_pieces_column(df):
    df["Nombre_pieces"] = pd.to_numeric(df["Nombre_pieces"], errors="coerce")
    return df

def clean_superficie_column(df):
    df["Superficie"] = pd.to_numeric(df["Superficie"], errors="coerce")
    return df

# Sélection du fichier
choix = st.sidebar.selectbox("Choisissez la catégorie de biens :", list(DATASETS.keys()))
df_path = DATASETS[choix]
df = load_data(df_path)

if df is not None:
    df.columns = df.columns.str.strip()

    if "Prix" in df.columns:
        df = clean_price_column(df)
        df = df[df["Prix"].notnull()]
    if "Nombre_pieces" in df.columns:
        df = clean_nombre_pieces_column(df)
        df = df[df["Nombre_pieces"].notnull()]
    if "Superficie" in df.columns:
        df = clean_superficie_column(df)
        df = df[df["Superficie"].notnull()]

    # Afficher quelques métriques
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total annonces", len(df))

    if "Prix" in df.columns:
        prix_moyen = df["Prix"].mean()
        prix_max = df["Prix"].max()
        col2.metric("Prix moyen", f"{prix_moyen:,.0f} FCFA", delta=f"Max: {prix_max:,.0f} FCFA")

    if "Nombre_pieces" in df.columns:
        pieces_moyen = df["Nombre_pieces"].mean()
        pieces_max = df["Nombre_pieces"].max()
        col3.metric("Nb pièces moyen", f"{pieces_moyen:.1f}", delta=f"Max: {pieces_max:.0f}")

    if "Superficie" in df.columns:
        superficie_moyenne = df["Superficie"].mean()
        superficie_max = df["Superficie"].max()
        col4.metric("Surface moyenne", f"{superficie_moyenne:,.0f} m²", delta=f"Max: {superficie_max:,.0f} m²")

    # Visualisation
    st.subheader("Analyse des données")
    viz_type = st.sidebar.selectbox("Outil de visualisation :", ["Plotly", "Matplotlib"])

    df_filtered = df.copy()

    if "Prix" in df.columns:
        min_price, max_price = st.sidebar.slider(
            "Filtrer par prix (FCFA):",
            min_value=int(df["Prix"].min()),
            max_value=int(df["Prix"].max()),
            value=(int(df["Prix"].quantile(0.1)), int(df["Prix"].quantile(0.9)))
        )
        df_filtered = df_filtered[df_filtered["Prix"].between(min_price, max_price)]

    if "Superficie" in df.columns:
        min_surface, max_surface = st.sidebar.slider(
            "Filtrer par superficie (m²):",
            min_value=int(df["Superficie"].min()),
            max_value=int(df["Superficie"].max()),
            value=(int(df["Superficie"].quantile(0.1)), int(df["Superficie"].quantile(0.9)))
        )
        df_filtered = df_filtered[df_filtered["Superficie"].between(min_surface, max_surface)]

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Prix", "Nombre de pièces", "Superficie"])

    with tab1:
        if "Prix" in df.columns:
            st.subheader("Distribution des Prix")
            if viz_type == "Plotly":
                fig1 = px.histogram(df_filtered, x='Prix', nbins=30,
                                    title="Répartition des Prix",
                                    color_discrete_sequence=['#636EFA'],
                                    labels={'Prix': 'Prix (FCFA)'})
                fig1.update_layout(bargap=0.1)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                plt.histplot(df_filtered['Prix'], bins=30, kde=True, ax=ax, color="orange")
                ax.set_xlabel("Prix (FCFA)")
                ax.set_ylabel("Nombre")
                ax.set_title("Distribution des Prix")
                st.pyplot(fig)

    with tab2:
        if "Nombre_pieces" in df.columns:
            st.subheader("Distribution du nombre de pièces")
            if viz_type == "Plotly":
                fig2 = px.histogram(df_filtered, x='Nombre_pieces', nbins=15,
                                    title="Répartition du nombre de pièces",
                                    color_discrete_sequence=['#00CC96'],
                                    labels={'Nombre_pieces': 'Nombre de pièces'})
                st.plotly_chart(fig2, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                plt.histplot(df_filtered['Nombre_pieces'], bins=15, kde=True, ax=ax, color="skyblue")
                ax.set_xlabel("Nombre de pièces")
                ax.set_ylabel("Fréquence")
                ax.set_title("Distribution des pièces")
                st.pyplot(fig)

    with tab3:
        if "Superficie" in df.columns:
            st.subheader("Distribution des Superficies")
            if viz_type == "Plotly":
                fig3 = px.histogram(df_filtered, x='Superficie', nbins=30,
                                    title="Répartition des Superficies",
                                    color_discrete_sequence=['#EF553B'],
                                    labels={'Superficie': 'Superficie (m²)'})
                fig3.update_layout(bargap=0.1)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                plt.histplot(df_filtered['Superficie'], bins=30, kde=True, ax=ax, color="#EF553B")
                ax.set_xlabel("Superficie (m²)")
                ax.set_ylabel("Nombre")
                ax.set_title("Distribution des Superficies")
                st.pyplot(fig)

    

    # Données 
    if st.checkbox("Afficher les données"):
        st.subheader("Données")
        st.dataframe(df_filtered)

else:
    st.error(f"Le fichier {df_path} n'existe pas ou n'a pas pu être chargé.")

