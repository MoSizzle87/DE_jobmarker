import json
from pathlib import Path


# Définition des correspondances entre les anciennes et les nouvelles clés
renaming_map = {
    "job_title": "title",
    "job_location": "location",
    "company_turnover": "turnover_in_millions",
    "company_industry": "sector",
    "Langages de Programmation": "ProgLanguage",
    "Bases de Données": "DataBase",
    "Analyse de Données": "DataAnalytics",
    "Big Data": "BigData",
    "Machine Learning et Data Mining": "MachineLearning",
    "Visualisation de Données": "DataVisualisation",
    "Statistiques": "Statistics",
    "Cloud Computing": "CloudComputing",
    "Outils de Développement": "DevTools",
    "Systèmes d'Exploitation": "OS",
    "Big Data et Processing": "SoftBigDataProcessing",
    "Automatisation et Orchestration": "Automation",
    "Infrastructure as Code (IaC)": "InfrastructureAsCode",
    "Sécurité et Réseau": "NetworkSecurty",
    "Outils de Collaboration": "Collaboration",
    "Compétences": "Other",
    "raw_description": "description"
}


current_path = Path(__file__).resolve().parent
doc_path = Path.joinpath(current_path, "old_databases", "indeed_final_db_bronze_v4.json")

# Initialiser une liste pour stocker chaque objet JSON
data = []

# Charger le fichier JSON ligne par ligne
with open(doc_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Charger l'objet JSON de la ligne courante
        obj = json.loads(line)

        # Ajouter la variable source avec la valeur "Indeed"
        obj["source"] = "Indeed"

        # Renommer chaque clé selon la correspondance
        for old_key, new_key in renaming_map.items():
            if old_key in obj:
                obj[new_key] = obj.pop(old_key)

        # Ajouter l'objet JSON à la liste
        data.append(obj)

output_doc = Path.joinpath(current_path, "data", "indeed_silver.json")
# Sauvegarder les modifications dans un nouveau fichier JSON
with open(output_doc, 'w', encoding='utf-8') as f:
    # Écrire chaque objet JSON dans le fichier, séparé par une virgule et une nouvelle ligne
    for i, obj in enumerate(data):
        json.dump(obj, f, ensure_ascii=False)
        # Ajouter une virgule après chaque objet sauf le dernier
        if i < len(data) - 1:
            f.write(',\n')
