# Corrections du Projet

# Démarrage du Projet

Pour démarrer le projet, suivez les étapes ci-dessous :

1. Assurez-vous d'être dans le répertoire du projet.

2. Installez les dépendances en exécutant la commande suivante dans votre terminal pour installer les paquets requis à partir du fichier requirements.txt :

   ```bash
   pip install -r requirements.txt

3. Une fois que les dépendances sont installées avec succès, vous pouvez démarrer l'application Flask en exécutant la commande suivante dans votre terminal :

    ```bash
    flask run

4. Après avoir exécuté la commande ci-dessus, vous devriez voir un message indiquant que le serveur Flask est démarré et qu'il écoute sur un port spécifique, par exemple :
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

5. Ouvrez votre navigateur web et accédez à l'URL indiquée dans le message, par exemple http://127.0.0.1:5000/, pour accéder à Services Montréal.

## Fonctionnalités et Tests


1. **(A1) Obtenir les données à partir du fichier CSV**
   - Données présentes dans la base de donnée db/violations.db, téléchargé à l'aide d'une fonction dans 
   'database.py' et de la création de table dans 'violations.sql'


1. **(A2) Rendu de la Page d'Accueil**
   - **Fonctionnalité :** Page d'accueil, moteur de recherche en fonction de nom d'établissement,
    propriétaire et rue.
   - **Test :** Ouvrir l'application dans un navigateur web. Une fois sur la page d'acceuil, entrez un mot correspondant aux éxigences dans le moteur de recherche et le résultat sera affiché sur une autre page.


16. **(A3) Planificateur**
    - **Fonctionnalité :** Planificateur de tâches périodiques en arrière-plan, mise à jour des données.
    - **Test :** Vous pouvez changer l'heure de mise à jour des données dans le fichier scheduler.py 
    à la fonction 'def start_scheduler():'. 
    Par exemple: 
    `scheduler.add_job(extract_and_update_data, 'cron', hour=14, minute=26)`


2. **(A4)(A5) Recherche par Date**
   - **Fonctionnalité :** Fonctionnalité pour rechercher des infractions basées sur des dates spécifiques.
   - **Test :** Accéder à la route '/par_date' et saisir des paramètres de date valides. 
    Sinon, entré l'url suivant :
    `/contrevenants?du=2022-05-08&au=2024-05-15`


3. **(A6) Recherche par Restaurants**
   - **Fonctionnalité :** Service pour rechercher des infractions par noms de restaurants.
   - **Test :** Aller à la route '/par_restaurants'. Sélectionner un restaurant et vérifier que les infractions liées à ce restaurant sont affichées.


4. **Infractions par Restaurant**
   - **Fonctionnalité :** Création d'une route pour retourner des données JSON contenant les infractions pour un restaurant spécifique.
   - **Test :** Accéder à la route '/infraction_par_restaurant' avec un paramètre de nom de restaurant valide. Vérifier que les données JSON avec les infractions pertinentes sont retournées.
   Exemple :
   '/infraction_par_restaurant?restaurant=RESTAURANT%20CHUAN%20XIANG%20QING'


5. **Service REST pour les Infractions**
   - **Fonctionnalité :** Développement d'une route pour récupérer les données d'infractions basées sur une plage de dates spécifiée.
   - **Test :** Utiliser un client REST pour envoyer des requêtes GET à la route '/contrevenants' avec des paramètres de date valides. S'assurer que les infractions pour la plage de dates spécifiée sont retournées.


6. **Route de Documentation RAML**
   - **Fonctionnalité :** Implémentation d'une route pour afficher la documentation RAML du service.
   - **Test :** Accéder à la route '/doc' dans un navigateur web. Vérifier que la documentation RAML est correctement affichée.


8. **(D1) Soumission du Formulaire de Plainte**
   - **Fonctionnalité :** Autorisation des utilisateurs à soumettre un formulaire de plainte, stockant les données dans une base de données SQLite.
   - **Test :** Remplir le formulaire de plainte et le soumettre. Vérifier que la plainte est stockée avec succès dans la base de données. Simplement en cliquant sur le bouton 'Afficher plaintes'.


9. **Affichage des Plaintes**
   - **Fonctionnalité :** Développement d'une route pour afficher toutes les plaintes soumises.
   - **Test :** Accéder à la route '/afficher_plaintes'. Vérifier qu'une liste des plaintes soumises est affichée.


10. **(D2) Suppression des Plaintes**
    - **Fonctionnalité :** Service REST pour supprimer des plaintes.
    - **Test :** Cocher une ou plusieurs checkbox de plaintes, puis appuyer sur le bouton 'Supprimer'. Observer la suppréssion.


11. **(C1) Liste des Établissements en Infraction**
    - **Fonctionnalité :** Route pour retourner une liste d'établissements avec le nombre d'infractions.
    - **Test :** Accéder à la route '/etablissements_infractions'. Vérifier qu'une réponse JSON contenant les établissements et le nombre d'infractions est retournée.


12. **(C2) Liste des Établissements en Infraction au Format XML**
    - **Fonctionnalité :** Route pour retourner une liste d'établissements avec le nombre d'infractions au format XML.
    - **Test :** Accéder à la route '/etablissements_infractions_xml'. Vérifier qu'une réponse XML contenant les établissements et le nombre d'infractions est retournée.


13. **(C3) Liste des Établissements en Infraction au Format CSV**
    - **Fonctionnalité :** Fourniture d'une route pour retourner une liste d'établissements avec le nombre d'infractions au format CSV.
    - **Test :** Accéder à la route '/etablissements_infractions_csv'. Vérifier qu'un fichier CSV contenant les établissements et le nombre d'infractions est téléchargé.


14. **Gestion des Erreurs 404**
    - **Fonctionnalité :** Page d'erreur 404 personnalisée pour traiter les erreurs de page non trouvée.
    - **Test :** Accéder à une route inexistante. Vérifier que la page d'erreur 404 personnalisée est affichée.











