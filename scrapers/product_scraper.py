import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = 'http://books.toscrape.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; EthicalScraper/1.0)'
}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    time.sleep(2)  # ethical delay
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    return BeautifulSoup(response.text, 'html.parser')

def scrape_book_data(book):
    title = book.h3.a['title']
    price = book.select_one('.price_color').text.strip()
    availability = book.select_one('.availability').text.strip()
    rating = book.select_one('p.star-rating')['class'][1]
    link = urljoin(BASE_URL, book.h3.a['href'])
    return {
        'title': title,
        'price': price,
        'availability': availability,
        'rating': rating,
        'product_url': link
    }

def scrape_all_books():
    all_books = []
    page = 1
    while True:
        print(f"Scraping page {page}...")
        url = urljoin(BASE_URL, f'catalogue/page-{page}.html')
        soup = get_soup(url)
        if soup is None or not soup.select('article.product_pod'):
            break

        books = soup.select('article.product_pod')
        for book in books:
            book_data = scrape_book_data(book)
            all_books.append(book_data)

        page += 1

    return all_books

import os

def save_to_csv(books, filename='data/scraped_products.csv'):
    # Create folder if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    keys = books[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)

    print(f"\n✅ Saved {len(books)} products to {filename}")


if __name__ == "__main__":
    books = scrape_all_books()
    if books:
        save_to_csv(books)
