document.getElementById('plainteForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);

    var jsonData = {
        nom_etablissement: formData.get('nom_etablissement'),
        adresse: formData.get('adresse'),
        ville: formData.get('ville'),
        date_visite: formData.get('date_visite'),
        nom_client: formData.get('nom_client'),
        description_probleme: formData.get('description_probleme')
    };

    var schema = {
        "type": "object",
        "properties": {
            "nom_etablissement": {"type": "string"},
            "adresse": {"type": "string"},
            "ville": {"type": "string"},
            "date_visite": {"type": "string", "format": "date"},
            "nom_client": {"type": "string"},
            "description_probleme": {"type": "string"}
        },
        "required": ["nom_etablissement", "adresse", "ville", "date_visite", "nom_client", "description_probleme"]
    };

    var errors = [];
    for (var key in schema.properties) {
        if (!(key in jsonData)) {
            errors.push("Le champ '" + key + "' est obligatoire.");
        }
    }

    if (errors.length > 0) {
        alert('Erreur de validation :\n' + errors.join('\n'));
    } else {
        fetch('/plainte', {
            method: 'POST',
            body: JSON.stringify(jsonData),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Plainte envoyée avec succès');
                window.location.href = '/'; 
            } else {
                throw new Error('Erreur lors de l\'envoi de la plainte');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Une erreur est survenue. Veuillez réessayer.');
        });
    }
});
