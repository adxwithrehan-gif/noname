import os
import json
import urllib.parse
import xml.etree.ElementTree as ET
import urllib.request
import google.generativeai as genai

# Gemini API Configuration
GEMINI_API_KEY = "AQ.Ab8RN6KvMwetPGe9EQ6NN_AY7btvM2kyCpI2VV5VtKxOOFXxnA"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def fetch_google_trends():
    rss_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    xml_data = response.read()

    root = ET.fromstring(xml_data)
    trending_posts = []

    for item in root.findall('.//item'):
        title = item.find('title').text
        traffic = item.find('{https://trends.google.com/trends/trendingsearches/daily}approx_traffic')
        traffic_val = traffic.text if traffic is not None else "0"

        # 10K+ Traffic Filter
        if "+" in traffic_val:
            count = int(traffic_val.replace("+", "").replace(",", ""))
            if count >= 10000:
                snippet = item.find('description').text if item.find('description') is not None else title
                trending_posts.append({"title": title, "traffic": traffic_val, "snippet": snippet})

    return trending_posts

def rewrite_with_gemini(news_item):
    prompt = f"""
    Rewrite the following news trend into a professional, unique, 100% copyright-free news article:
    Title: {news_item['title']}
    Context: {news_item['snippet']}
    
    Provide the output in valid JSON format:
    {{
      "headline": "Catchy Title",
      "summary": "Brief summary",
      "content": "Full detailed article text...",
      "category": "Entertainment/Global"
    }}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return None

def save_news():
    trends = fetch_google_trends()
    processed_news = []

    for item in trends[:5]: # Top 5 Trends
        ai_article = rewrite_with_gemini(item)
        if ai_article:
            processed_news.append(ai_article)

    os.makedirs('data/news', exist_ok=True)
    with open('data/news/latest_news.json', 'w') as f:
        json.dump(processed_news, f, indent=2)

if __name__ == "__main__":
    save_news()
