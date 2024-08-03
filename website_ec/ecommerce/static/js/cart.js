document.addEventListener('DOMContentLoaded', function() {
    const updateBtns = document.getElementsByClassName('update-cart');
    console.log('Update buttons:', updateBtns); // Log the update buttons to ensure they are being selected

    for (let i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function() {
            const productId = this.dataset.product;
            const action = this.dataset.action;

            console.log('Product ID:', productId); // Log the product ID to ensure it's being captured
            console.log('Action:', action); // Log the action to ensure it's being captured

            fetch('/update_item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    'productId': productId,
                    'action': action
                })
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then((data) => {
                console.log('Data:', data);
                // Reload the page
                window.location.reload();
            })
            .catch(error => console.error('Error:', error));
        });
    }

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
