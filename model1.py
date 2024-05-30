import pandas as pd
from repository import get_config
from openpyxl import load_workbook
from openpyxl.styles import Alignment

def calcul(sorted_df):
    "définir une fonction pour ensuite l'utiliser dans streamlit"
    # Appel de la fonction pour obtenir les données
    sorted_df = get_config()

    # Filtrer les années uniques
    years = sorted_df['Date'].unique()
    years.sort()

    # Dictionnaire pour stocker l'EPS de chaque année
    eps_dict = {}

    # Initialiser les listes pour stocker les résultats
    data = {
         "Year": [],
         "Current Ratio": [],
         "Current Ratio Interpretation": [],
         "Leverage Ratio": [],
         "Leverage Ratio Interpretation": [],
         "ROE": [],
         "ROE Interpretation": [],
         "EPS": [],
         "EPS Interpretation": [],
         "PER": [],
         "PER Interpretation": [],
         "ROCE": [],
         "ROCE Interpretation": []
         }

    # Calculer et interpréter les ratios pour chaque année
    for year in years:
        # Filtrer le DataFrame pour l'année spécifique
        df_year = sorted_df[sorted_df['Date'] == year]

        # Calcul du current ratio pour l'année spécifique
        total_current_assets = df_year.loc[df_year['Class'] == 'Total Current Assets', 'Amount (in thousands of $)'].iloc[0]
        total_current_liabilities = df_year.loc[df_year['Class'] == 'Total Current Liabilities', 'Amount (in thousands of $)'].iloc[0]
        current_ratio = round(total_current_assets / total_current_liabilities, 2)

        # Interprétation du current ratio
        if current_ratio < 1:
            current_interpretation = "Potential liquidity risk. The company could have difficulty hedging its short-term obligations."
        elif 1 <= current_ratio < 2:
            current_interpretation = "Adequate hedging of short-term bonds. The company manages its liquidity well."
        elif 2 <= current_ratio < 2.5:
            current_interpretation = "The financial situation is good. The company has a comfortable margin of security for its short-term debts."
        else:
            current_interpretation = "Excessively high ratio, possible inefficient use of assets."

        # Calcul du leverage ratio pour l'année spécifique
        total_debt = df_year.loc[df_year['Class'] == 'Total Debt', 'Amount (in thousands of $)'].iloc[0]
        total_equity = df_year.loc[df_year['Class'] == 'Total Equity', 'Amount (in thousands of $)'].iloc[0]
        leverage_ratio = round(total_debt / total_equity, 2)

        # Interprétation du leverage ratio
        if leverage_ratio < 0.5:
            leverage_interpretation = "Low debt. The company makes little use of debt, which could indicate an underutilization of financing opportunities."
        elif 0.5 <= leverage_ratio < 1:
            leverage_interpretation = "Moderate debt. The company has a good balance between debt and equity, reflecting prudent management of financial risks."
        elif 1 <= leverage_ratio < 2:
            leverage_interpretation = "High debt. The company is heavily dependent on debt, increasing its financial risks."
        else:
            leverage_interpretation = "The company is highly indebted, which considerably increases its financial risks."

        # Calcul du ROE pour l'année spécifique
        net_income = df_year.loc[df_year['Class'] == 'Net income', 'Amount (in thousands of $)'].iloc[0]
        roe = round(net_income / total_equity, 2)

        # Interprétation du ROE
        if roe < 0.05:
            roe_interpretation = "Low profitability. The company is not using its equity effectively to generate income."
        elif 0.05 <= roe < 0.15:
            roe_interpretation = "Acceptable profitability. The company generates reasonable returns."
        elif 0.15 <= roe < 0.25:
            roe_interpretation = "The company is efficient in using equity capital to produce profits."
        else:
            roe_interpretation = "Excellent profitability. The company excels at maximizing return on equity, indicating superior management."

        # Calcul de l'EPS pour l'année spécifique
        num_shares = df_year.loc[df_year['Class'] == 'Number of Shares', 'Amount (in thousands of $)'].iloc[0]
        eps = round(net_income / num_shares, 2)
        eps_dict[year] = eps

        # Interprétation de l'EPS en le comparant avec l'année précédente
        if year - 1 not in eps_dict:
            eps_interpretation = "No data from last year to compare."
        else:
            previous_eps = eps_dict[year - 1]
            if eps > previous_eps:
                eps_interpretation = "EPS on the rise, indicating an increase in the company's profitability, usually a positive sign that can attract investors."
            elif eps == previous_eps:
                eps_interpretation = "The company maintains its profitability. The stability of the EPS can indicate the prudent management and a well-established company."
            else:
                eps_interpretation = "EPS in decline. Potential problems in the company's operations or profitability recovery."

        # Calcul du PER pour l'année spécifique
        market_price_per_share = df_year.loc[df_year['Class'] == 'Market Price Per Share', 'Amount (in thousands of $)'].iloc[0]
        per = round(market_price_per_share / eps, 2) if eps != 0 else float('inf')

        # Interprétation du PER
        if per < 10:
            per_interpretation = "The stock is undervalued, which may indicate a buying opportunity or an expectation of lower earnings."
        elif 10 <= per < 20:
            per_interpretation = "The stock is realistically valued, reflecting average market expectations."
        elif 20 <= per < 30:
            per_interpretation = "The stock is slightly over-priced, indicating that investors are anticipating earnings growth."
        else:
            per_interpretation = "The stock is heavily over-priced, signifying a strong speculation on future earnings growth."

        # Calcul du ROCE pour l'année spécifique
        operating_income = df_year.loc[df_year['Class'] == 'Operating income', 'Amount (in thousands of $)'].iloc[0]
        total_assets = df_year.loc[df_year['Class'] == 'Total Assets', 'Amount (in thousands of $)'].iloc[0]
        total_current_liabilities = df_year.loc[df_year['Class'] == 'Total Current Liabilities', 'Amount (in thousands of $)'].iloc[0]
        roce = round(operating_income / (total_assets - total_current_liabilities), 2)

        # Interprétation du ROCE
        if roce < 0.05:
            roce_interpretation = "Low yield. This indicates that the company is not very efficient in using its capital to generate revenue."
        elif 0.05 <= roce < 0.1:
            roce_interpretation = "Moderate performance. The company uses its capital in a reasonable manner to generate income."
        elif 0.1 <= roce < 0.15:
            roce_interpretation = "Good performance. The company is quite efficient in using its capital to produce profits."
        else:
            roce_interpretation = "Excellent performance. The company is very efficient in the use of its capital, managing profits in relation to the capital employed."

        # Ajouter les résultats aux listes
        data["Year"].append(year)
        data["Current Ratio"].append(current_ratio)
        data["Current Ratio Interpretation"].append(current_interpretation)
        data["Leverage Ratio"].append(leverage_ratio)
        data["Leverage Ratio Interpretation"].append(leverage_interpretation)
        data["ROE"].append(roe)
        data["ROE Interpretation"].append(roe_interpretation)
        data["EPS"].append(eps)
        data["EPS Interpretation"].append(eps_interpretation)
        data["PER"].append(per)
        data["PER Interpretation"].append(per_interpretation)
        data["ROCE"].append(roce)
        data["ROCE Interpretation"].append(roce_interpretation)

    # Créer un DataFrame à partir des résultats
    results_df = pd.DataFrame(data)

    # Transposer le DataFrame
    results_df = results_df.set_index("Year").transpose()
    return results_df