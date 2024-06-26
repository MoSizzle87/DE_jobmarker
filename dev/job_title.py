import json


JOBS = {
    "data engineer": (("data", "engineer"), ("data", "ingénieur")),
    "data architect": (("data", "architect"), ("architect", "si"), ("architect", "it")),
    "data scientist": (("data", "scientist"), ("science", "donnée")),
    "data analyst": (("data", "analyst"), ("data", "analytics")),
    "software engineer": (("software", "engineer"), ("software", "developer"), ("développeur", "logiciel"), ("ingénieur", "logiciel")),
    "devops": ("devops",),
    "data warehousing engineer": ("data", "warehouse", "engineer"),
    "machine learning engineer": (("machine", "learning", "engineer"), ("ml", "engineer")),
    "cloud architect /engineer ": (("cloud", "architect"), ("cloud", "engineer"), ("cloud", "ingénieur"), ("cloud", "engineer"), ("AWS",), ("GCP",), ("azure",)),
    "solution architect": ("solution", "architect"),
    "big data engineer": (("big", "data", "engineer"), ("ingénieur", "big", "data")),
    "big data developer": (("big", "data", "developer"), ("développeur", "big", "data")),
    "data infrastructure engineer": ("data", "infrastructure", "engineer"),
    "data pipeline engineer": ("data", "pipeline", "engineer"),
    "etl developer": ("etl",),
    "business developer": (("business", "developer"), ("sales", "developer")),
    "business analyst": ("business", "analyst"),
    "cybersecurity": (("cyber", "security"), ("cyber", "sécurité"), ("cyber", "risk"), ("cyber", "risque")),
    "sysops": ("sysops",),
    "consultant data": ("data", "consultant"),
        }

json_file = "C:/Users/GASSAMA/Downloads/indeed_gold.json"


def find_job_title(title, jobs_dict):
    title_lower = title.lower()

    for job, keywords in jobs_dict.items():
        if isinstance(keywords[0], tuple):
            for keyword_tuple in keywords:
                if all(word in title_lower for word in keyword_tuple):
                    return job
        else:
            if all(word in title_lower for word in keywords):
                return job

    return "Other"


with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for entry in data:
    title = entry.get('title', '')
    if title:
        entry['job_title_bis'] = find_job_title(title.lower(), JOBS)
    else:
        entry['job_title_bis'] = "Other"

output_json_file = "C:/Users/GASSAMA/Downloads/indeed_gold_updated.json"

with open(output_json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Les données mises à jour ont été sauvegardées dans {output_json_file}")