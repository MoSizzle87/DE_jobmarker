import json
from pathlib import Path

current_path = Path(__file__).resolve().parent
doc_path = Path.joinpath(current_path, "data", "wttj_database_bronze.json")
# Charger le fichier JSON
with open(doc_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Parcourir chaque entrée dans la liste de dictionnaires
for entry in data:
    # 1 - Supprimer 'job'
    if 'job' in entry:
        del entry['job']

    # 2 - Renommer 'skill_categories' en 'skills'
    if 'skill_categories' in entry:
        entry['skills'] = entry.pop('skill_categories')

    # 3 - Supprimer le dictionnaire 'contract_data' et transformer ses variables en simples colonnes
    if 'contract_data' in entry:
        contract_data = entry.pop('contract_data')
        for key, value in contract_data.items():
            entry[key] = value

    # 4 - Renommer 'job_title' en 'title'
    if 'job_title' in entry:
        entry['title'] = entry.pop('job_title')

    # 5 - Renommer 'job_description' en 'description'
    if 'raw_description' in entry:
        entry['description'] = entry.pop('raw_description')

    # 6 - Modifier les valeurs de 'link' pour ajouter la chaîne de caractères 'https://www.welcometothejungle.com'
    if 'link' in entry:
        entry['link'] = 'https://www.welcometothejungle.com' + entry['link']

    # 7 - Renommer 'Data Analytics' en 'DataAnalytics' dans 'skills'
    if 'skills' in entry and 'Data Analytics' in entry['skills']:
        entry['skills']['DataAnalytics'] = entry['skills'].pop('Data Analytics')

output_doc = Path.joinpath(current_path, "data", "wttj_database_silver.json")
# Sauvegarder les modifications dans un nouveau fichier JSON
with open(output_doc, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
