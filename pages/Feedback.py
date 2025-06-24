import streamlit as st
import requests
import json
from datetime import datetime
from streamlit.components.v1 import html

# Configuration KoboToolbox
KOBO_API_URL = "https://kobo.humanitarianresponse.info/api/v2/assets/"
KOBO_TOKEN = st.secrets["KOBO_TOKEN"]
ASSET_UID = st.secrets["ASSET_UID"]

st.title("⭐ Évaluation de l'application")

# Création d'onglets pour choisir entre formulaire intégré ou iframe
tab1, tab2 = st.tabs(["Formulaire Streamlit", "Formulaire KoboToolbox"])

with tab1:
    with st.form("kobo_evaluation_form"):
        # Section 1: Informations personnelles
        st.header("1. Informations personnelles")
        name = st.text_input("Nom complet (optionnel)")
        email = st.text_input("Email (optionnel)")
        
        # Section 2: Évaluation principale
        st.header("2. Évaluation de l'application")
        rating = st.slider("Note globale (1 = Très mauvais, 5 = Excellent)", 1, 5, 3,)
        
        col1, col2 = st.columns(2)
        with col1:
            experience = st.selectbox("Expérience globale", 
                                    ["", "Exceptionnelle", "Bonne", "Moyenne", "Médiocre"])
        with col2:
            recommendation = st.selectbox("Recommanderiez-vous l'application?",
                                        ["", "Certainement", "Probablement", "Peut-être", "Non"])
        
        # Section 3: Fonctionnalités
        st.header("3. Fonctionnalités utilisées")
        features = st.multiselect("Quelles fonctionnalités avez-vous utilisées?",
                                ["Scraping de données", "Téléchargement des données", 
                                 "Tableau de bord"])
        
        # Section 4: Commentaires
        st.header("4. Commentaires")
        positive = st.text_area("Ce que vous avez aimé")
        improvements = st.text_area("Suggestions d'amélioration")
        additional = st.text_area("Autres commentaires")
        
        # Soumission
        submitted = st.form_submit_button("Soumettre l'évaluation")
        
        if submitted:
            # Construction du payload
            submission_data = {
                "nom": name,
                "email": email,
                "note": rating,
                "experience": experience,
                "recommendation": recommendation,
                "features": ", ".join(features),
                "positive": positive,
                "improvements": improvements,
                "additional": additional,
                "date_evaluation": datetime.now().isoformat()
            }
            
            payload = {
                "submission": submission_data
            }
            
            headers = {
                "Authorization": f"Token {KOBO_TOKEN}",
                "Content-Type": "application/json"
            }
            
            try:
                # Envoi à KoboToolbox
                response = requests.post(
                    f"{KOBO_API_URL}{ASSET_UID}/submissions/",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 201:
                    st.success("""
                    ### Merci pour votre évaluation! ✅
                    Votre feedback a été enregistré avec succès.
                    """)
                    st.balloons()
                else:
                    st.error(f"""
                    ### Erreur d'envoi ❌
                    Code: {response.status_code}  
                    Message: {response.text}
                    """)
                    
            except Exception as e:
                st.error(f"""
                ### Erreur de connexion
                {str(e)}
                """)

with tab2:
    st.header("Formulaire KoboToolbox")
    st.markdown("""
    **Remplissez directement notre formulaire optimisé :**
    """)
    
    # Intégration de l'iframe KoboToolbox
    kobo_iframe = """
    <iframe 
        src="https://ee.kobotoolbox.org/i/ncOeJVUx" 
        width="100%" 
        height="600"
        frameborder="0"
        style="border:none; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1)"
        allowfullscreen
    ></iframe>
    """
    html(kobo_iframe, height=600)
    
    st.markdown("""
    <div style="margin-top:20px; padding:15px; background:#f0f2f6; border-radius:10px">
    <p>Problème d'affichage ? <a href="https://ee.kobotoolbox.org/i/ncOeJVUx" target="_blank">Ouvrir dans un nouvel onglet</a></p>
    </div>
    """, unsafe_allow_html=True)

# Section commune aux deux onglets
st.info("""
**Votre avis compte !** Merci de nous aider à améliorer l'application.
""")