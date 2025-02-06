# Cette classe fournit des méthodes pour interagir avec la base de données
# des violations. Elle permet de télécharger et
# d'insérer des données depuis une URL,
# ainsi que de récupérer des informations sur les contraventions,
# les restaurants et les infractions à partir de la base de données.


import sqlite3
import csv
import requests


# Fonction pour télécharger les données depuis l'URL
# et les insérer dans la base de données
def telecharger_et_inserer_donnees(url, db_file):
    response = requests.get(url)
    if response.status_code == 200:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        csv_data = response.text.splitlines()
        csv_reader = csv.reader(csv_data, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            cursor.execute(
                "REPLACE INTO violations "
                "(id_poursuite, business_id, date, description, adresse, date_jugement, "
                "etablissement, montant, proprietaire, ville, statut, date_statut, categorie) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                row
            )

        conn.commit()
        conn.close()
        print("Données insérées avec succès dans la base de données.")
    else:
        print("Erreur lors du téléchargement des données.")


# Fonction qui récupère le nombre de contraventions pour
# chaque établissement entre deux dates spécifiées
def get_contraventions_between_dates(date_debut, date_fin):
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT etablissement, COUNT(*) as nombre_contraventions "
        "FROM violations "
        "WHERE date BETWEEN ? AND ? "
        "GROUP BY etablissement",
        (date_debut, date_fin)
    )

    contraventions = cursor.fetchall()

    conn.close()

    return contraventions


# Fonction qui récupère la liste des restaurants
# à partir de la base de données des violations
def get_restaurants():
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT etablissement FROM violations")
    restaurants = cursor.fetchall()
    conn.close()
    return [restaurant[0] for restaurant in restaurants]


# Fonction qui récupère toutes les infractions pour un restaurant donné
def get_infractions_par_restaurant(nom_restaurant):
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * "
        "FROM violations "
        "WHERE etablissement=?",
        (nom_restaurant,)
    )

    infractions = cursor.fetchall()
    conn.close()
    return infractions


# Fonction qui récupère toutes les violations à partir de la base de données
def get_violations_from_database():
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM violations")
    violations = cursor.fetchall()
    conn.close()
    return violations


if __name__ == "__main__":
    url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"
    db_file = "db/violations.db"
    telecharger_et_inserer_donnees(url, db_file)
