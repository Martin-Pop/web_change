import requests
import hashlib
from bs4 import BeautifulSoup

def get_page_hash(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        html_content = response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    for script in soup(["script", "style", "meta", "noscript"]):
        script.extract()

    clean_text = soup.get_text(strip=True)
    content_hash = hashlib.sha256(clean_text.encode('utf-8')).hexdigest()

    return content_hash