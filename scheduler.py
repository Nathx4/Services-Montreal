from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import sqlite3
import database
import csv


# URL des données à extraire
url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"
db_file = "db/violations.db"


# Fonction qui télécharge les données depuis l'URL spécifiée
# et les insère dans la base de données
def extract_and_update_data():
    database.telecharger_et_inserer_donnees(url, db_file)
    print("Données mises à jour avec succès à :", datetime.now())


# Fonction qui initialise un planificateur d'arrière-plan
# et ajoute une tâche pour mettre à jour les données à minuit chaque jour.
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(extract_and_update_data, 'cron', hour=0)
    scheduler.start()
