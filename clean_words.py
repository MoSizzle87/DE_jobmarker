import json
import os
import re

json_file = "/Users/MoG/repo/DE_jobmarket/wttj/data/wttj_database_gold_bis.json"

# Vérifiez si le fichier existe et n'est pas vide
if not os.path.isfile(json_file) or os.path.getsize(json_file) == 0:
    raise FileNotFoundError(f"Le fichier {json_file} est introuvable ou vide.")

# Liste de mots de référence
reference_words = [
    "AWS",
    "Adaptability",
    "Airflow",
    "Alibaba Cloud",
    "Ansible",
    "Apache Airflow",
    "Apache Flink",
    "Apache Kafka",
    "Avro",
    "Azure",
    "Backend Development",
    "Bash",
    "Bayesian Statistics",
    "Big Data",
    "Big Query",
    "BigQuery",
    "C#",
    "C++",
    "CI / CD",
    "CI/CD",
    "Cassandra",
    "CatBoost",
    "Chef",
    "Cloud",
    "CloudFormation",
    "Collaboration",
    "Communication",
    "Confluence",
    "Creativity",
    "Critical Thinking",
    "Databricks",
    "DevOps",
    "Discord",
    "Docker",
    "Elasticsearch",
    "Empathy",
    "Firewall",
    "Flexibility",
    "Flink",
    "GCP",
    "Git",
    "Google Cloud Platform",
    "HBase",
    "Hadoop",
    "Hyper-V",
    "IBM Cloud",
    "Inférentielles",
    "Initiative",
    "Interpersonal Skills",
    "JIRA",
    "Java",
    "Jenkins",
    "Json",
    "Julia",
    "Keras",
    "Kotlin",
    "Kubernetes",
    "Leadership",
    "LightGBM",
    "Linux",
    "MATLAB",
    "ML",
    "MacOS",
    "Machine Learning",
    "Matplotlib",
    "Microsoft Teams",
    "MongoDB",
    "MySQL",
    "Neo4j",
    "NoSQL",
    "NumPy",
    "OpenShift",
    "Oracle SQL",
    "Orange",
    "Organization",
    "Pandas",
    "Plotly",
    "PostgreSQL",
    "Power BI",
    "Problem Solving",
    "Protocol Buffers",
    "Puppet",
    "PyTorch",
    "Python",
    "R",
    "SQL",
    "SQL Server",
    "SSL/TLS",
    "Scala",
    "Scikit-Learn",
    "Seaborn",
    "SingleStore",
    "Slack",
    "Snowflake",
    "Spark",
    "Statistiques",
    "Statistiques Bayésiennes",
    "Statistiques Descriptives",
    "Stress Management",
    "Tableau",
    "Teams",
    "Teamwork",
    "TensorFlow",
    "Terraform",
    "Time Management",
    "Travis CI",
    "VMware",
    "VPN",
    "VirtualBox",
    "Windows",
    "Wireshark",
    "XGBoost",
    "XML",
]

# Convertir la liste de mots de référence en minuscules
reference_words_lower = [word.lower() for word in reference_words]


# Fonction pour nettoyer et remplacer une liste de mots
def nettoyer_et_remplacer_liste(liste):
    if liste is None:
        return None
    nettoye = []
    for mot in liste:
        mot_nettoye = re.sub(r"[^\w\s]", "", mot).strip().lower()
        if len(mot_nettoye) < 4:
            for ref_word, ref_word_lower in zip(reference_words, reference_words_lower):
                if re.fullmatch(ref_word_lower, mot_nettoye):
                    nettoye.append(ref_word)
                    break
            else:
                nettoye.append(mot_nettoye)
        else:
            for ref_word, ref_word_lower in zip(reference_words, reference_words_lower):
                if ref_word_lower in mot_nettoye:
                    nettoye.append(ref_word)
                    break
            else:
                nettoye.append(mot_nettoye)
    return list(set([mot for mot in nettoye if mot]))  # Supprimer les doublons


try:
    # Charger le fichier JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"Erreur lors de la lecture du fichier JSON: {e}")

# Parcourir les compétences et nettoyer les listes
for job in data:
    if "skills" in job:
        for skill_category, skill_list in job["skills"].items():
            job["skills"][skill_category] = nettoyer_et_remplacer_liste(skill_list)

# Sauvegarder le fichier JSON nettoyé
with open("data_nettoye.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(
    "Les compétences ont été nettoyées et le fichier a été sauvegardé sous 'data_nettoye.json'."
)
