# web_search.py
import requests
from bs4 import BeautifulSoup

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
        text = g.get_text()
        if text:  # בדיקת תוכן
            results.append(text)
    
    return results[:5]  # נחזיר את 5 התוצאות הראשונות
