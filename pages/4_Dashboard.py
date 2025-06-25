import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration de la page
st.set_page_config(
    page_title="Dashboard CoinAfrique", 
    layout="wide", 
    page_icon="📊"
)
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

# Nettoyage des colonnes numériques
def clean_numeric_column(df, column_name):
    if column_name in df.columns:
        df[column_name] = pd.to_numeric(
            df[column_name].astype(str).str.replace(r'[^\d.]', '', regex=True),
            errors="coerce"
        )
        df = df[df[column_name].notnull()]
    return df

# Sélection du fichier
choix = st.sidebar.selectbox(
    "Choisissez la catégorie de biens :", 
    list(DATASETS.keys())
)
df_path = DATASETS[choix]
df = load_data(df_path)

if df is not None:
    # Nettoyage des données
    df.columns = df.columns.str.strip()
    df = clean_numeric_column(df, "Prix")
    df = clean_numeric_column(df, "Nombre_pieces")
    df = clean_numeric_column(df, "Superficie")

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

    # Filtres interactifs
    st.sidebar.header("Filtres")
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
    
    if "Nombre_pieces" in df.columns:
        min_pieces, max_pieces = st.sidebar.slider(
            "Filtrer par nombre de pièces:",
            min_value=int(df["Nombre_pieces"].min()),
            max_value=int(df["Nombre_pieces"].max()),
            value=(int(df["Nombre_pieces"].quantile(0.1)), int(df["Nombre_pieces"].quantile(0.9)))
        )
        df_filtered = df_filtered[df_filtered["Nombre_pieces"].between(min_pieces, max_pieces)]

    # Tabs pour les visualisations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Distribution des Prix", 
        "Nombre de pièces", 
        "Superficie",
        "Relations"
    ])

    with tab1:
        if "Prix" in df.columns:
            st.subheader("Distribution des Prix")
            fig = px.histogram(
                df_filtered, 
                x="Prix",
                nbins=30,
                title="Distribution des Prix",
                labels={"Prix": "Prix (FCFA)"},
                color_discrete_sequence=["#636EFA"],
                marginal="box"
            )
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if "Nombre_pieces" in df.columns:
            st.subheader("Distribution du nombre de pièces")
            fig = px.histogram(
                df_filtered,
                x="Nombre_pieces",
                nbins=15,
                title="Distribution du nombre de pièces",
                labels={"Nombre_pieces": "Nombre de pièces"},
                color_discrete_sequence=["#00CC96"],
                text_auto=True
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if "Superficie" in df.columns:
            st.subheader("Distribution des Superficies")
            fig = px.histogram(
                df_filtered,
                x="Superficie",
                nbins=30,
                title="Distribution des Superficies",
                labels={"Superficie": "Superficie (m²)"},
                color_discrete_sequence=["#EF553B"],
                marginal="rug"
            )
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Relations entre variables")
        if "Prix" in df.columns and "Superficie" in df.columns:
            fig = px.scatter(
                df_filtered,
                x="Superficie",
                y="Prix",
                color="Nombre_pieces" if "Nombre_pieces" in df.columns else None,
                title="Relation Prix vs Superficie",
                hover_data=["Prix", "Superficie", "Nombre_pieces"] if "Nombre_pieces" in df.columns else None
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Les colonnes nécessaires pour cette visualisation ne sont pas disponibles")

    # Affichage des données
    if st.checkbox("Afficher les données filtrées"):
        st.subheader("Données filtrées")
        st.dataframe(
            df_filtered,
            column_config={
                "Prix": st.column_config.NumberColumn(format="%,d FCFA"),
                "Superficie": st.column_config.NumberColumn(format="%,d m²")
            },
            use_container_width=True
        )

    # Téléchargement des données
    st.sidebar.download_button(
        label="Télécharger les données filtrées",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name=f"biens_immobiliers_{choix.lower()}_filtres.csv",
        mime="text/csv"
    )

else:
    st.error(f"Le fichier {df_path} n'existe pas ou n'a pas pu être chargé.")
    st.info("Veuillez vérifier que le scraping a été effectué au préalable.")