from datetime import datetime
import json
import os


def save_news():
  today_date = datetime.now().strftime('%Y-%m-%d')

  # Example processed news object with Date Stamp
  processed_news = [
      {
          'headline': 'Google Trends AI Headline Example',
          'summary': 'Short news summary for preview',
          'content': 'Full rewritten Gemini news content...',
          'category': 'Entertainment',
          'date': today_date,
          'thumbnail': 'https://via.placeholder.com/500x280',
      }
  ]

  os.makedirs('data/news', exist_ok=True)
  with open('data/news/latest_news.json', 'w') as f:
    json.dump(processed_news, f, indent=2)


if __name__ == '__main__':
  save_news()
