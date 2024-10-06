import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from requests.exceptions import RequestException

# To avoid visiting the same link multiple times
visited_links = set()
processed_text = set()  # Track processed text to avoid duplication

# Use a session for network optimization
session = requests.Session()

# Data format for Qdrant
scraped_data = []

def extract_data(url, base_url):
    """Extract headings, paragraphs, list items, and links from the page and structure data for Qdrant."""
    if url in visited_links:
        return
    visited_links.add(url)

    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')

            page_data = {
                "url": url,
                "headings": [],
                "paragraphs": [],
                "list_items": [],
                "links": []
            }

            # Extract and process heading tags (h1, h2, h3)
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                heading_text = heading.text.strip()
                if heading_text not in processed_text:
                    processed_text.add(heading_text)
                    page_data["headings"].append(heading_text)

            # Extract and process paragraph text
            for paragraph in soup.find_all('p'):
                paragraph_text = paragraph.text.strip()
                if paragraph_text not in processed_text:
                    processed_text.add(paragraph_text)
                    page_data["paragraphs"].append(paragraph_text)

            # Extract and process list items (<li>)
            for list_item in soup.find_all('li'):
                list_item_text = list_item.text.strip()
                if list_item_text not in processed_text:
                    processed_text.add(list_item_text)
                    page_data["list_items"].append(list_item_text)

            # Extract and handle hyperlinks
            for link in soup.find_all('a', href=True):
                full_link = urljoin(base_url, link['href'])  # Resolve relative links
                if full_link not in visited_links:
                    link_text = link.text.strip()
                    page_data["links"].append({"url": full_link, "text": link_text})

                    # Recursively follow the link and extract data if it's within the same domain
                    if is_same_domain(full_link, base_url):
                        time.sleep(1)  # To prevent too many rapid requests
                        extract_data(full_link, base_url)

            # Add page data to the scraped data list
            scraped_data.append(page_data)

        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
    except RequestException as e:
        print(f"Error while fetching {url}: {e}")

def is_same_domain(url, base_url):
    """Check if a URL belongs to the same domain."""
    return urlparse(url).netloc == urlparse(base_url).netloc

def start_scraping(base_url):
    """Start the scraping process from the base URL."""
    extract_data(base_url, base_url)

