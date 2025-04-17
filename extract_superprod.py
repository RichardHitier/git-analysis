
import json
from datetime import datetime

# Fonction pour convertir timestamp en date lisible
def ts_to_date(ts):
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Chargement du fichier JSON
with open('super_productivity_20250417.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraction des projets
projects = data['project']['entities']

# Parcours et affichage des infos demandées
for project_id, project in projects.items():
    title = project.get('title', 'Sans titre')
    work_start = project.get('workStart', {})
    work_end = project.get('workEnd', {})

    print(f"📁 Projet : {title}")
    for date_str in sorted(work_start.keys()):
        start_ts = work_start[date_str]
        end_ts = work_end.get(date_str)
        start = ts_to_date(start_ts)
        end = ts_to_date(end_ts) if end_ts else 'Non défini'
        print(f"  - {date_str}: start = {start}, end = {end}")
    print()
