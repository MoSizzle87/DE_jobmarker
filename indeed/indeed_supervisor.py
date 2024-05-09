import time
import subprocess


def check_links(file):
    with open(file, 'r') as f:
        contenu = f.read().strip()
    return bool(contenu)  # Vérifie si le contenu du fichier est vide ou non


def restart_supervisor_process():
    # Commande pour redémarrer le processus Supervisor
    subprocess.run(['sudo', 'service', 'supervisor', 'restart'])


# Nom du fichier contenant les liens
job_links = '/home/mosizzle/repositories/formation_project/DE_jobmarket/indeed/data/job_links.txt'

while check_links(job_links):
    print("Le fichier de liens n'est pas vide. Attente avant de vérifier à nouveau.")
    time.sleep(60)  # Attendre 60 secondes avant de vérifier à nouveau

print("Le fichier de liens est vide. Arrêt du script.")
