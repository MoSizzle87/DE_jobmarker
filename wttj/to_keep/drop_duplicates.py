import json
from pathlib import Path

current_path = Path(__file__).resolve().parent
doc_path = Path.joinpath(current_path, "data", "wttj_database_silver.json")
# Charger le fichier JSON
with open(doc_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Nombre d'entrées avant la suppression des doublons :", len(data))

# Créer un ensemble pour stocker les données vues (en excluant la variable 'link')
seen_data = set()

# Parcourir chaque entrée dans la liste de dictionnaires
unique_entries = []

for entry in data:
    # Exclure la variable 'link' lors de la détermination des doublons
    entry_without_link = entry.copy()
    if 'link' in entry_without_link:
        del entry_without_link['link']

    # Convertir le dictionnaire en une chaîne JSON pour identifier les doublons
    json_str = json.dumps(entry_without_link, sort_keys=True)
    if json_str not in seen_data:
        unique_entries.append(entry)
        seen_data.add(json_str)

print("Nombre d'entrées après la suppression des doublons :", len(unique_entries))

output_doc = Path.joinpath(current_path, "data", "wttj_database_gold.json")
# Sauvegarder les modifications dans un nouveau fichier JSON
with open(output_doc, 'w', encoding='utf-8') as f:
    json.dump(unique_entries, f, ensure_ascii=False, indent=4)
