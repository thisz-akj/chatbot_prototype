// static/js/search.js

document.addEventListener('DOMContentLoaded', function() {
    const searchBox = document.getElementById('search-box');
    const resultsDiv = document.getElementById('search-results');
    const csrftoken = getCookie('csrftoken');

    searchBox.addEventListener('input', function() {
        const query = searchBox.value;

        if (query.length < 2) {
            resultsDiv.innerHTML = ''; // Clear results if the query is too short
            return;
        }

        fetch(`/search/?q=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.text())
        .then(data => {
            resultsDiv.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
