
    function liveSearch() {
        let input = document.getElementById('searchInput').value.toLowerCase();
        let cards = document.getElementsByClassName('card');
        for (let i = 0; i < cards.length; i++) {
            let title = cards[i].innerText.toLowerCase();
            cards[i].style.display = title.includes(input) ? "block" : "none";
        }
    }

    function subscribeUser() {
        let email = document.getElementById('subEmail').value;
        if(email) {
            alert('Thank you for subscribing to MediaDB!');
            document.getElementById('subEmail').value = '';
        }
    }
    