const deleteButton = document.getElementById('deleteButton');

deleteButton.addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('input[name="plainte"]:checked');
    const ids = Array.from(checkboxes).map(checkbox => checkbox.value);

    fetch('/supprimer_plaintes', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ids: ids })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); 
        window.location.reload();
    })
    .catch(error => console.error('Erreur lors de la suppression des plaintes:', error));
});
