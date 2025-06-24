import requests
from bs4 import BeautifulSoup

def scrape_site(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Exemple de scraping - à adapter
        data = []
        for item in soup.select('.product-item'):  # Sélecteur à modifier
            data.append({
                'title': item.select_one('.title').text if item.select_one('.title') else None,
                'price': item.select_one('.price').text if item.select_one('.price') else None
            })
        return data
    except Exception as e:
        print(f"Erreur de scraping: {e}")
        return []