import os
import requests
import streamlit as st
from loguru import logger

# ---------------------------------------------------
# Logging
# ---------------------------------------------------
logger.add("/logs/streamlit.log", rotation="500 MB")

# ---------------------------------------------------
# Titre de l'application
# ---------------------------------------------------
st.title("Frontend - Interaction avec FastAPI")

# ---------------------------------------------------
# URL de l'API
# ---------------------------------------------------
api_url = os.getenv("API_URL", "http://api:8080")

# ---------------------------------------------------
# Champ de saisie et bouton
# ---------------------------------------------------
val = st.text_input("Entrez une valeur à envoyer à l'API")

if st.button("Envoyer"):
    if not val:
        st.warning("Veuillez entrer une valeur avant d'envoyer.")
    else:
        try:
            # Appel POST à l'API FastAPI
            res = requests.post(f"{api_url}/predict", data={"data": val})
            res.raise_for_status()  # Vérifie si la réponse HTTP est OK
            st.subheader("Résultat de la prédiction :")
            st.json(res.json())
            logger.info(f"Appel API réussi avec la valeur : {val}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de l'appel API : {e}")
            logger.error(f"Erreur appel API avec {val} : {e}")