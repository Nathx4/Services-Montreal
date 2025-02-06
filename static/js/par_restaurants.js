document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var restaurant = document.getElementById('restaurant').value;

    var url = '/infraction_par_restaurant?restaurant=' + encodeURIComponent(restaurant);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var results = document.getElementById('resultsRestaurant');
            results.innerHTML = '<h2>Infractions pour le restaurant ' + restaurant + ' :</h2>';

            if (data.length > 0) {
                var table = '<table><thead><tr><th>ID poursuite</th><th>Date</th><th>Description</th></tr></thead><tbody>';
                data.forEach(function(infraction) {
                    table += '<tr><td>' + infraction[0] + '</td><td>' + infraction[2] + '</td><td>' + infraction[3] + '</td></tr>';
                });
                table += '</tbody></table>';
                results.innerHTML += table;
            } else {
                results.innerHTML += '<p>Aucune infraction trouvée pour ce restaurant.</p>';
            }
        })
        .catch(error => console.error('Erreur lors de la recherche:', error));
});
