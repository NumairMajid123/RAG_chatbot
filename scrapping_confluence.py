######test this
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse
import os
import json
import re

BASE_URL = 'https://docs.expertflow.com/'
START_URL = 'https://docs.expertflow.com/?l=en'
OUTPUT_DIR = 'scraped_pages_final'
os.makedirs(OUTPUT_DIR, exist_ok=True)
seen_links = set()


def fetch_and_parse(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return None


def extract_links(url):
    soup = fetch_and_parse(url)
    if not soup:
        return set()
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if not href or href.startswith('#') or 'createpage.action' in href or 'login.action' in href:
            continue
        if any(href.lower().endswith(ext) for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.zip']):
            continue
        full_url = urljoin(url, href)
        full_url, _ = urldefrag(full_url)
        if full_url.startswith(BASE_URL):
            links.add(full_url)
    return links


def extract_tables(table):
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['th', 'td'])
        row = [cell.get_text(strip=True) for cell in cells]
        if row:
            rows.append(row)
    return rows


def extract_content(soup, page_url):
    content = []
    main_content = soup.find(id='main-content')
    if not main_content:
        return content

    current_section = None

    def process_element(el, section):
        if el.name == 'p':
            section['content'].append({'type': 'paragraph', 'text': el.get_text(strip=True)})
        elif el.name in ['ul', 'ol']:
            section['content'].append({'type': 'list', 'items': [li.get_text(strip=True) for li in el.find_all('li')]})
        elif el.name == 'table':
            section['content'].append({'type': 'table', 'rows': extract_tables(el)})
        elif el.name in ['div', 'section', 'article']:
            for child in el.find_all(recursive=False):
                process_element(child, section)

    for element in main_content.find_all(recursive=False):
        if element.name in ['h1', 'h2', 'h3']:
            if current_section:
                content.append(current_section)
            current_section = {
                'header': element.get_text(strip=True),
                'level': element.name,
                'content': [],
                'url': page_url
            }
        elif current_section is None:
            current_section = {
                'header': soup.title.string.strip() if soup.title else "Untitled",
                'level': 'h2',
                'content': [],
                'url': page_url
            }
            process_element(element, current_section)
        else:
            process_element(element, current_section)

    if current_section:
        content.append(current_section)

    return content


def save_content(content, filename):
    json_path = os.path.join(OUTPUT_DIR, f"{filename}.json")
    txt_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
    with open(txt_path, 'w', encoding='utf-8') as f:
        for section in content:
            f.write(f"{section['level'].upper()}: {section['header']}\n")
            f.write("-" * len(section['header']) + "\n")
            for item in section['content']:
                if item['type'] == 'paragraph':
                    f.write(f"\n{item['text']}\n")
                elif item['type'] == 'list':
                    f.write("\n- " + "\n- ".join(item['items']) + "\n")
                elif item['type'] == 'table':
                    rows = item['rows']
                    if rows:
                        max_cols = max(len(row) for row in rows)
                        f.write("\n| " + " | ".join([f"Col{i + 1}" for i in range(max_cols)]) + " |\n")
                        f.write("| " + " | ".join(["---"] * max_cols) + " |\n")
                        for row in rows:
                            padded = row + [""] * (max_cols - len(row))
                            f.write("| " + " | ".join(padded) + " |\n")
            f.write("\n" + "=" * 50 + "\n")


def scrape_recursive(url, base_prefix):
    if url in seen_links or not url.startswith(base_prefix):
        return
    seen_links.add(url)
    print(f"🔍 Scraping: {url}")
    soup = fetch_and_parse(url)
    if not soup:
        return
    content = extract_content(soup, url)
    if content:
        filename = urlparse(url).path.strip('/').replace('/', '_') or 'index'
        save_content(content, filename)
    for link in extract_links(url):
        scrape_recursive(link, base_prefix=base_prefix)


def detect_latest_versions():
    links = extract_links(START_URL)
    version_map = {}
    version_pattern = re.compile(r'/([\w-]+)/(\d+(?:\.\d+)+)/?$')

    for link in links:
        match = version_pattern.search(link)
        if match:
            product, version_str = match.groups()
            version_tuple = tuple(map(int, version_str.split('.')))
            if product not in version_map or version_tuple > version_map[product][0]:
                version_map[product] = (version_tuple, link)
    print("\n Latest versions detected:")
    for k, v in version_map.items():
        print(f"{k} → {v[1]}")
    return [v[1] for v in version_map.values()]


if __name__ == "__main__":
    print("🔍 Fetching all links from home page...")
    latest_urls = detect_latest_versions()
    print("\n🚀 Starting scraping...")
    for url in latest_urls:
        scrape_recursive(url, base_prefix=url)

# if __name__ == "__main__":
#     test_url = "https://docs.expertflow.com/cx/4.8/cisco-contact-center-integration"
#     print(f"🔍 Testing single page: {test_url}")
#     soup = fetch_and_parse(test_url)
#     if soup:
#         content = extract_content(soup, test_url)
#         if content:
#             filename = urlparse(test_url).path.strip('/').replace('/', '_') or 'index'
#             save_content(content, filename)
#             print(" Done saving content.")
#         else:
#             print(" No content extracted.")
#     else:
#         print(" Could not fetch page.")