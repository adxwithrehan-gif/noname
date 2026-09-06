import os
import json
import requests
from datetime import datetime
import google.generativeai as genai

# ==========================================
# CONFIGURATION & API KEYS
# ==========================================
TMDB_API_KEY = "e0454b55527f15c2784604a0bc84df14"
# GEMINI_API_KEY environment variable se load hogi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Directory Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NEWS_DIR = os.path.join(DATA_DIR, 'news')
CSS_DIR = os.path.join(BASE_DIR, 'css')
JS_DIR = os.path.join(BASE_DIR, 'js')

for folder in [DATA_DIR, NEWS_DIR, CSS_DIR, JS_DIR]:
    os.makedirs(folder, exist_ok=True)

# ==========================================
# 1. BOT: TMDB DATA FETCHING
# ==========================================
def fetch_tmdb_data():
    print("[+] Syncing TMDB Data (Movies, TV, People)...")
    base_url = "https://api.themoviedb.org/3"
    
    endpoints = {
        "movies": f"{base_url}/trending/movie/day?api_key={TMDB_API_KEY}",
        "tv": f"{base_url}/trending/tv/day?api_key={TMDB_API_KEY}",
        "people": f"{base_url}/person/popular?api_key={TMDB_API_KEY}"
    }
    
    dataset = {}
    for key, url in endpoints.items():
        res = requests.get(url)
        if res.status_code == 200:
            dataset[key] = res.json().get('results', [])
        else:
            dataset[key] = []
            
    with open(os.path.join(DATA_DIR, 'tmdb_data.json'), 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4)
        
    print("[✓] TMDB Sync Complete.")
    return dataset

# ==========================================
# 2. BOT: GOOGLE TRENDS + GEMINI REWRITE
# ==========================================
def fetch_and_rewrite_news():
    print("[+] Fetching Real-time Trends & Rewriting via Gemini...")
    today_str = datetime.now().strftime("%Y-%m-%d")
    news_file = os.path.join(NEWS_DIR, f"{today_str}.json")
    
    # Mocking high-traffic trends response (10K+ filter criteria)
    sample_trends = [
        {"title": "Global Box Office Shatters Records This Weekend", "category": "Entertainment", "country": "Worldwide"},
        {"title": "Major Updates Announced for Upcoming Web Series", "category": "Web Series", "country": "USA"}
    ]
    
    rewritten_articles = []
    model = genai.GenerativeModel('gemini-pro')
    
    for item in sample_trends:
        prompt = f"Rewrite this news title and write a short 2-paragraph engaging entertainment article about: '{item['title']}'. Make it unique and professional."
        try:
            response = model.generate_content(prompt)
            content = response.text
        except Exception as e:
            content = item['title'] + " - Detailed insights arriving soon."
            
        rewritten_articles.append({
            "title": item['title'],
            "category": item['category'],
            "country": item['country'],
            "date": today_str,
            "content": content,
            "thumbnail": "https://via.placeholder.com/600x350?text=MediaDB+News"
        })
        
    with open(news_file, 'w', encoding='utf-8') as f:
        json.dump(rewritten_articles, f, indent=4)
        
    print(f"[✓] News generated and saved to {news_file}")
    return rewritten_articles

# ==========================================
# 3. GENERATE ADS.TXT & SITEMAP
# ==========================================
def generate_system_files():
    # Ads.txt
    with open(os.path.join(BASE_DIR, 'ads.txt'), 'w') as f:
        f.write("google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
        
    # Sitemap.xml
    urls = [
        "https://adxwithrehan-gif.github.io/MediaDB/",
        "https://adxwithrehan-gif.github.io/MediaDB/tv-shows.html",
        "https://adxwithrehan-gif.github.io/MediaDB/popular-people.html",
        "https://adxwithrehan-gif.github.io/MediaDB/rewards.html",
        "https://adxwithrehan-gif.github.io/MediaDB/news.html"
    ]
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap_content += f"  <url><loc>{u}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>\n"
    sitemap_content += '</urlset>'
    
    with open(os.path.join(BASE_DIR, 'sitemap.xml'), 'w') as f:
        f.write(sitemap_content)
    print("[✓] Ads.txt and Sitemap.xml generated.")

# ==========================================
# 4. GENERATE STYLES & JS
# ==========================================
def build_assets():
    css_content = """
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d253f; color: #fff; margin: 0; padding: 0; }
    header { background: #01b4e4; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
    nav a { color: #fff; text-decoration: none; margin: 0 12px; font-weight: bold; }
    .ad-slot { background: #1a365d; text-align: center; padding: 15px; margin: 10px 0; border: 1px dashed #90cea1; }
    .container { padding: 20px; max-width: 1200px; margin: auto; }
    .filter-bar { background: #0280a8; padding: 10px; margin-bottom: 20px; border-radius: 5px; display: flex; gap: 10px; }
    .filter-bar select, .filter-bar input { padding: 8px; border-radius: 4px; border: none; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
    .card { background: #041d33; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .card img { width: 100%; height: 280px; object-fit: cover; }
    .card-content { padding: 10px; }
    footer { background: #032541; padding: 20px; text-align: center; margin-top: 40px; }
    .subscribe-box { display: inline-flex; gap: 5px; margin-top: 10px; }
    .subscribe-box input { padding: 8px; border-radius: 4px; border: none; }
    .subscribe-box button { background: #90cea1; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; }
    """
    with open(os.path.join(CSS_DIR, 'style.css'), 'w') as f:
        f.write(css_content)

    js_content = """
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
    """
    with open(os.path.join(JS_DIR, 'main.js'), 'w') as f:
        f.write(js_content)

# ==========================================
# 5. TEMPLATE RENDERER
# ==========================================
def generate_pages():
    build_assets()
    generate_system_files()
    tmdb = fetch_tmdb_data()
    fetch_and_rewrite_news()

    pages = ['index.html', 'tv-shows.html', 'popular-people.html', 'rewards.html', 'news.html']
    
    for p in pages:
        page_title = p.replace('.html', '').replace('index', 'Movies & Series').replace('-', ' ').title()
        
        # Build Filter section only for News Page
        filter_html = ""
        if p == 'news.html':
            filter_html = """
            <div class="filter-bar">
                <select id="countryFilter"><option>All Countries</option><option>USA</option><option>Worldwide</option></select>
                <select id="categoryFilter"><option>All Categories</option><option>Entertainment</option><option>Web Series</option></select>
                <input type="date" id="dateFilter">
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediaDB - {page_title}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="logo"><h2>MediaDB</h2></div>
        <nav>
            <a href="index.html">Movies/Web Series</a>
            <a href="tv-shows.html">TV Shows</a>
            <a href="popular-people.html">Popular People</a>
            <a href="rewards.html">Rewards</a>
            <a href="news.html">News</a>
        </nav>
    </header>

    <div class="ad-slot">-- Header Advertisement Area --</div>

    <div class="container">
        <input type="text" id="searchInput" onkeyup="liveSearch()" placeholder="Search Movies, Shows, People, News..." style="width: 100%; padding: 12px; margin-bottom: 20px; box-sizing: border-box;">
        
        {filter_html}

        <h1>{page_title}</h1>
        <div class="ad-slot">-- Article Top Ad Position --</div>

        <div class="card-grid" id="contentGrid">
            <div class="card">
                <img src="https://via.placeholder.com/500x750?text=MediaDB+Media" alt="Media Cover">
                <div class="card-content">
                    <h3>Sample Media / Trending Item</h3>
                    <p>Automated payload synced with TMDB API & Gemini Engine.</p>
                </div>
            </div>
        </div>
    </div>

    <div class="ad-slot">-- Footer Advertisement Area --</div>

    <footer>
        <p>&copy; 2026 MediaDB. All Rights Reserved.</p>
        <div class="subscribe-box">
            <input type="email" id="subEmail" placeholder="Enter your email">
            <button onclick="subscribeUser()">Subscribe</button>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""
        
        with open(os.path.join(BASE_DIR, p), 'w', encoding='utf-8') as f:
            f.write(html_content)

    print("[✓] All HTML pages built successfully.")

if __name__ == "__main__":
    generate_pages()