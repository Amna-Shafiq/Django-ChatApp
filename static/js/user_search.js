// user_search.js

// JavaScript code to filter and display users based on search query
const searchInput = document.getElementById('searchInput');
const userCards = document.getElementById('userCards').children;

searchInput.addEventListener('input', function() {
  const query = searchInput.value.toLowerCase();

  for (let i = 0; i < userCards.length; i++) {
    const userCard = userCards[i];
    const username = userCard.querySelector('h5').textContent.toLowerCase();

    if (username.includes(query)) {
      userCard.style.display = 'block';
    } else {
      userCard.style.display = 'none';
    }
  }
});
