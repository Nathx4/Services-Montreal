# Cette classe définit les routes et les services REST
# pour une application Web Flask de Services Montréal.
# Elle permet de gérer les fonctionnalités liées aux plaintes,
# aux contraventions, aux restaurants,
# ainsi qu'à l'affichage et au téléchargement des données depuis la base de données.


from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for, Response
import sqlite3
import database
import atexit
from scheduler import start_scheduler
from jsonschema import validate
import xml.etree.ElementTree as ET
import csv


app = Flask(__name__)


start_scheduler()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/par_date', methods=['GET'])
def recherche_date():
    return render_template('par_date.html')


# Service REST recherche par nom de restaurants
@app.route('/par_restaurants', methods=['GET'])
def recherche_restaurants():
    restaurants = database.get_restaurants()
    return render_template('par_restaurants.html', restaurants=restaurants)


@app.route('/infraction_par_restaurant', methods=['GET'])
def infraction_par_restaurant():
    nom_restaurant = request.args.get('restaurant')

    infractions = database.get_infractions_par_restaurant(nom_restaurant)

    return jsonify(infractions)


# Service REST recherche par date
@app.route('/contrevenants')
def get_contraventions():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')

    contraventions = database.get_contraventions_between_dates(
        date_debut, date_fin)

    return jsonify(contraventions)


# Route pour afficher la documentation RAML
@app.route('/doc')
def show_raml_documentation():
    with open('documentation.html', 'r') as file:
        documentation_html = file.read()

    return documentation_html


# Resultat service REST du moteur de recherche
@app.route('/resultats', methods=['GET', 'POST'])
def resultats():
    if request.method == 'POST':
        recherche = request.form['recherche']
        conn = sqlite3.connect('db/violations.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM violations
            WHERE etablissement LIKE ?
            OR proprietaire LIKE ?
            OR adresse LIKE ?
        """, ('%' + recherche + '%',
              '%' + recherche + '%',
              '%' + recherche + '%'))

        resultats = cursor.fetchall()
        conn.close()
        return render_template('resultats.html', resultats=resultats)
    return render_template('resultats.html')


# Route pour soumettre le formulaire de plainte
@app.route('/plainte', methods=['POST'])
def submit_complaint_form():
    data = request.json
    nom_etablissement = data['nom_etablissement']
    adresse = data['adresse']
    ville = data['ville']
    date_visite = data['date_visite']
    nom_client = data['nom_client']
    description_probleme = data['description_probleme']

    conn = sqlite3.connect('db/plaintes.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO plaintes
    (nom_etablissement,
     adresse, ville, date_visite, nom_client, description_probleme)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            nom_etablissement,
            adresse,
            ville,
            date_visite,
            nom_client,
            description_probleme
        )
    )
    conn.commit()
    conn.close()

    return render_template('plainte.html')


# Route pour afficher le formulaire de plainte
@app.route('/plainte', methods=['GET'])
def show_complaint_form():
    return render_template('plainte.html')


# Route pour afficher toutes les plaintes
@app.route('/afficher_plaintes', methods=['GET'])
def afficher_plaintes():
    conn = sqlite3.connect('db/plaintes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plaintes")
    plaintes = cursor.fetchall()

    conn.close()

    return render_template('afficher_plaintes.html', plaintes=plaintes)


# Service REST suppression de plaintes
@app.route('/supprimer_plaintes', methods=['DELETE'])
def supprimer_plaintes():
    data = request.json
    ids = data.get('ids', [])

    conn = sqlite3.connect('db/plaintes.db')
    cursor = conn.cursor()

    for plainte_id in ids:
        cursor.execute("DELETE FROM plaintes WHERE id = ?", (plainte_id,))

    conn.commit()

    conn.close()

    return jsonify({"message": "Plaintes supprimées avec succès"}), 200


# Route pour obtenir la liste des établissements ayant commis des infractions
@app.route('/etablissements_infractions', methods=['GET'])
def etablissements_infractions():
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT etablissement, COUNT(*) AS nombre_infractions
        FROM violations
        GROUP BY etablissement
        ORDER BY nombre_infractions DESC
    """)
    resultats = cursor.fetchall()
    conn.close()

    reponse = [{"nom_etablissement": row[0], "nombre_infractions": row[1]} for row in resultats]
    return jsonify(reponse), 200


# Route pour obtenir la liste des établissements
# ayant commis des infractions au format XML
@app.route('/etablissements_infractions_xml', methods=['GET'])
def etablissements_infractions_xml():
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT etablissement, COUNT(*) AS nombre_infractions
        FROM violations
        GROUP BY etablissement
        ORDER BY nombre_infractions DESC
    """)
    resultats = cursor.fetchall()
    conn.close()

    root = ET.Element("etablissements_infractions")
    for row in resultats:
        etablissement = ET.SubElement(root, "etablissement")
        nom = ET.SubElement(etablissement, "nom_etablissement")
        nom.text = row[0]
        nombre_infractions = ET.SubElement(etablissement, "nombre_infractions")
        nombre_infractions.text = str(row[1])

    xml_str = ET.tostring(root, encoding='utf-8', method='xml')

    return Response(xml_str, mimetype='text/xml')


# Même route pour obtenir au format CSV (télécharge un fichier CSV)
@app.route('/etablissements_infractions_csv', methods=['GET'])
def etablissements_infractions_csv():
    conn = sqlite3.connect('db/violations.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT etablissement, COUNT(*) AS nombre_infractions
        FROM violations
        GROUP BY etablissement
        ORDER BY nombre_infractions DESC
    """)
    resultats = cursor.fetchall()
    conn.close()

    csv_data = "nom_etablissement,nombre_infractions\n"
    for row in resultats:
        csv_data += f"{row[0]},{row[1]}\n"

    response = Response(csv_data, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=etablissements_infractions.csv'
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
