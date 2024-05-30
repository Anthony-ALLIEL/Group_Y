import pandas as pd
import os

def get_config():
    file_name = "iRobot.xlsx"
    file_path = "/Users/antho/Desktop/PROJECT/"
    excel_path = os.path.join(file_path, file_name)

    print("Chargement du fichier Excel depuis le chemin :", excel_path)

    df = pd.read_excel(excel_path, sheet_name="DataBase")
    print("Données chargées avec succès.")

    # Filtrer les lignes du DataFrame en fonction des classes nécessaires
    required_classes = [
        "Total Current Assets",
        "Total Current Liabilities",
        "Net income",
        "Total Equity",
        "Total Debt",
        "Number of Shares",
        "Market Price Per Share",
        "Operating income",
        "Total Assets"
    ]
    filtered_df = df[df['Class'].isin(required_classes)]

    # Trier le DataFrame filtré par la colonne 'Class'
    sorted_df = filtered_df.sort_values(by='Class')

    # Afficher les cinq premières lignes du DataFrame
    print(sorted_df.head())

    return sorted_df
