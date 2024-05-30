import os
import pandas as pd
import streamlit as st

import repository
import model1

def get_file_list(extension, path):
    """Obtenez tous les fichiers avec une extension spécifique sous le chemin spécifié"""
    if not os.path.isdir(path):
        return path, []
    file_list = [f for f in os.listdir(path) if f.endswith(extension)]
    return path, file_list

st.title("Analyse financière d'une entreprise")
default_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = st.sidebar.text_input(
    "Veuillez entrer dans le répertoire où se trouvent les données",
    value=default_dir,
    key="data_dir"
)

# Chemin de mise à jour
path = input_folder

# Obtenez tous les fichiers .xlsx dans le répertoire spécifié
path, file_list_xlsx = get_file_list(".xlsx", path)

# Si un fichier .xlsx existe, affichez le composant de téléchargement de fichier
if file_list_xlsx:
    uploaded_file = st.sidebar.file_uploader("Uploader un fichier .xlsx", type=["xlsx"])

    # Si un utilisateur télécharge un fichier
    if uploaded_file is not None:
        # read Excel
        df = pd.read_excel(uploaded_file)

        # Afficher le contenu du fichier
        st.write("Contenu du fichier uploadé :")
        st.write(df)

    if uploaded_file is not None:
        # Utilisez la fonction de calcul pour traiter les fichiers téléchargés et obtenir DataFrame
        result = model1.calcul(uploaded_file)

        options = {
            "2020": False,
            "2021": False,
            "2022": False
        }
        for option in options:
            options[option] = st.sidebar.checkbox(option)

        if options["2020"]:
            st.write(result.iloc[:, 0])

        if options["2021"]:
           st.write(result.iloc[:, 1])

        if options["2022"]:
           st.write(result.iloc[:, 2])


else:
    st.sidebar.write("Aucun fichier.xlsx trouvé dans le répertoire.")
    st.write("Veuillez entrer un répertoire valide contenant des fichiers .xlsx.")





