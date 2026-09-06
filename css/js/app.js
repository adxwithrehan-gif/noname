const TMDB_API_KEY = 'e0454b55527f15c2784604a0bc84df14';
const BASE_URL = 'https://api.themoviedb.org/3';
const IMG_URL = 'https://image.tmdb.org/t/p/w500';

let currentPage = 'movies';

function switchPage(page, btn) {
  currentPage = page;
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  if(btn) btn.classList.add('active');

  const filterBar = document.getElementById('newsFilterBar');
  filterBar.style.display = (page === 'news') ? 'flex' : 'none';

  if (page === 'news') {
    loadNewsData();
  } else {
    fetchTMDBData(page);
  }
}

async function fetchTMDBData(type) {
  const content = document.getElementById('contentArea');
  content.innerHTML = '<p>Fetching data from TMDB Engine...</p>';

  let endpoint = '/trending/movie/day';
  if (type === 'tv') endpoint = '/trending/tv/day';
  if (type === 'people') endpoint = '/person/popular';
  if (type === 'rewards') endpoint = '/movie/top_rated';

  try {
    const res = await fetch(`${BASE_URL}${endpoint}?api_key=${TMDB_API_KEY}`);
    const data = await res.json();
    renderCards(data.results, type);
  } catch (err) {
    content.innerHTML = '<p>Error fetching TMDB Data.</p>';
  }
}

function renderCards(items, type) {
  const content = document.getElementById('contentArea');
  content.innerHTML = items.map(item => {
    const title = item.title || item.name;
    const poster = (item.poster_path || item.profile_path) ? `${IMG_URL}${item.poster_path || item.profile_path}` : 'https://via.placeholder.com/500x750';
    return `
      <div class="card" onclick="openDetails('${type}', ${item.id})">
        <img src="${poster}" alt="${title}">
        <div class="card-body">
          <div class="card-title">${title}</div>
          <small style="color:#01b4e4;">⭐ ${item.vote_average ? item.vote_average.toFixed(1) : 'Popular'}</small>
        </div>
      </div>
    `;
  }).join('');
}

async function handleLiveSearch(event) {
  const query = event.target.value.trim();
  if (query.length < 2) return;

  const content = document.getElementById('contentArea');
  const res = await fetch(`${BASE_URL}/search/multi?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}`);
  const data = await res.json();
  renderCards(data.results, 'search');
}

// Subscription & Tracking Logic
async function handleSubscribe() {
  const emailInput = document.getElementById('subEmail');
  const status = document.getElementById('subStatus');
  const email = emailInput.value.trim();

  if (!email || !email.includes('@')) {
    status.innerText = "Please enter a valid email address.";
    status.style.color = "#ff6b6b";
    return;
  }

  try {
    const geoRes = await fetch('https://ipapi.co/json/');
    const geoData = await geoRes.json();
    
    const subscriberData = {
      email: email,
      country: geoData.country_name || "Unknown",
      countryCode: geoData.country_code || "XX",
      subscribedAt: new Date().toISOString()
    };

    console.log("Subscriber Captured:", subscriberData);
    status.innerText = `Subscribed successfully from ${subscriberData.country}!`;
    status.style.color = "#90cea1";
    emailInput.value = "";
  } catch (e) {
    status.innerText = "Subscribed successfully!";
    status.style.color = "#90cea1";
  }
}

function closeModal() {
  document.getElementById('detailsModal').style.display = 'none';
}

switchPage('movies');
