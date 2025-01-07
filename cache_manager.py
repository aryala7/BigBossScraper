import os
import json
import time
from scrapy import Selector
import requests

CACHE_FILE_PRODUCTS = "products.json"
CACHE_FILE_FLIESE = "fliese.json"
CACHE_EXPIRATION = 60 * 15  # 15 minutes

def fetch_and_cache(base_url, headers, cache_file, parse_function):
    all_products = []
    page = 1

    while True:
        url = base_url.format(page=page)
        response = requests.get(url, headers=headers)
        print(f"Fetching page {page}: Status code {response.status_code}")

        if response.status_code != 200:
            break  # Exit loop if the page does not exist or access is denied

        products = parse_function(response.text)
        if not products:
            print("No more products found. Exiting pagination.")
            break

        all_products.extend(products)
        page += 1

    with open(cache_file, 'w') as f:
        json.dump({"timestamp": time.time(), "data": all_products}, f)

    return all_products

def parse_products(response_text):
    sel = Selector(text=response_text)
    image_urls = sel.xpath("//div[@class='image_box']/img/@src").getall()
    titles = sel.xpath('//div[@class=\"content_box\"]/h2/a/text()').getall()
    return [{"image_url": img, "title": title} for img, title in zip(image_urls, titles)]

def parse_fliese(response_text):
    sel = Selector(text=response_text)
    image_urls = sel.xpath("//figure[contains(@class, 'ld-sp-img')]//img/@data-src").getall()
    titles = sel.xpath("//div[@class='ld-sp-info']/h3/a/text()").getall()
    return [{"image_url": img, "title": title} for img, title in zip(image_urls, titles)]

def fetch_and_cache_products():
    base_url = "https://sahandjam.com/page/{page}/?s&post_type=product"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    return fetch_and_cache(base_url, headers, CACHE_FILE_PRODUCTS, parse_products)

def fetch_and_cache_fliese():
    base_url = "https://tabriztilegroup.com/products/page/{page}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    return fetch_and_cache(base_url, headers, CACHE_FILE_FLIESE, parse_fliese)

def get_cached_data(cache_file, fetch_function):
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            if time.time() - cache["timestamp"] < CACHE_EXPIRATION:
                return cache["data"]
    return fetch_function()

def get_cached_products():
    return get_cached_data(CACHE_FILE_PRODUCTS, fetch_and_cache_products)

def get_cached_fliese():
    return get_cached_data(CACHE_FILE_FLIESE, fetch_and_cache_fliese)

# Exported constants
get_cached_products.cache_file = CACHE_FILE_PRODUCTS
get_cached_fliese.cache_file = CACHE_FILE_FLIESE
