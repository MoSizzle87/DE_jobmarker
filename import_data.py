import json
from pathlib import Path
from elasticsearch import Elasticsearch, helpers

# Connexion à Elasticsearch
es = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=('elastic', 'pf-HI8FJKzF+uWn+*OGb'),
    ca_certs=False,
    verify_certs=False)

# Nom de l'index où les données seront importées
index_name = 'jobmarket'

# Dossiers contenant les fichiers JSON
directories = [
        Path('/Users/MoG/repo/DE_jobmarket/wttj/Database_to_use'),
        Path('/Users/MoG/repo/DE_jobmarket/indeed/data')
        ]

# Fonction pour lire le fichier JSON
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Fonction pour transformer les données JSON en actions pour Elasticsearch
def generate_actions(data, index_name):
    for record in data:
        yield {
            "_index": index_name,
            "_source": record
        }

# Vérifiez si l'index existe déjà
if es.indices.exists(index=index_name):
    print(f"Index '{index_name}' already exists.")
else:
    # Créer l'index
    es.indices.create(index=index_name)
    print(f"Index '{index_name}' created.")

# Parcourir chaque dossier et importer les fichiers JSON
for directory in directories:
    for file_path in directory.glob('*.json'):
        print(f"Importing {file_path}...")
        data = read_json(file_path)
        helpers.bulk(es, generate_actions(data, index_name))
        print(f"Imported {file_path} successfully.")

print(f"All data imported into index '{index_name}' successfully.")

