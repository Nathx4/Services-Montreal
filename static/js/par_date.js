document.getElementById('searchDate').addEventListener('submit', function(event) {
    event.preventDefault();

    var startDate = document.getElementById('startDate').value;
    var endDate = document.getElementById('endDate').value;

    var url = '/contrevenants?du=' + startDate + '&au=' + endDate;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var results = document.getElementById('resultsDate');
            results.innerHTML = '<h2>Résultats de la recherche :</h2>';

            if (data.length > 0) {
                var table = '<table><thead><tr><th>Nom de l\'établissement</th><th>Nombre de contraventions</th></tr></thead><tbody>';
                data.forEach(function(item) {
                    table += '<tr><td>' + item[0] + '</td><td>' + item[1] + '</td></tr>';
                });
                table += '</tbody></table>';
                results.innerHTML += table;
            } else {
                results.innerHTML += '<p>Aucune contravention trouvée pour cette période de temps.</p>';
            }
        })
        .catch(error => console.error('Erreur lors de la recherche:', error));
});

