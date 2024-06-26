import json
from collections import Counter

json_file = "C:/Users/GASSAMA/Downloads/indeed_gold_updated.json"

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

job_title_bis_values = [entry['job_title_bis'] for entry in data]
counter = Counter(job_title_bis_values)

for job_title, count in counter.items():
    print(f"{job_title}: {count}")

import pandas as pd

df = pd.DataFrame(counter.items(), columns=['job_title_bis', 'count'])
print(df)

"""for entry in data:
    if entry['job_title_bis'] == "Other":
        print(entry.get('title', 'Titre inconnu'))"""