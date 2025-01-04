import os
import json
import time
import random
from threading import Thread
from flask import Flask,render_template
from scrapy import Selector
import requests
app = Flask(__name__)

CACHE_FILE_FILESE = "fliese.json"
CACHE_FILE = "products.json"
CACHE_EXPIRATION = 60 * 15 #15 minutes 

def fetch_and_cache_products():
    base_url = "https://sahandjam.com/page/{page}/?s&post_type=product"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    }
    all_products = []
    page = 1

    while True:
        url = base_url.format(page=page)
        response = requests.get(url, headers=headers)
        print(f"Fetching page {page}: Status code {response.status_code}")
        
        if response.status_code != 200:
            break  # Exit loop if the page does not exist or access is denied

        sel = Selector(text=response.text)
        image_urls = sel.xpath("//div[@class='image_box']/img/@src").getall()
        titles = sel.xpath('//div[@class="content_box"]/h2/a/text()').getall()

        if not image_urls and not titles:
            # Stop if no products are found (indicating the last page has been reached)
            print("No more products found. Exiting pagination.")
            break
        
        # Combine the products for the current page
        products = [{"image_url": img, "title": title} for img, title in zip(image_urls, titles)]
        all_products.extend(products)

        # Go to the next page
        page += 1

    # Cache the data
    with open(CACHE_FILE, 'w') as f:
        json.dump({"timestamp": time.time(), "data": all_products}, f)

    return all_products


def fetch_and_cache_fliese():
    base_url  = "https://tabriztilegroup.com/products/page/{page}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36",
    }
    all_products = []
    page = 1

    while True:
        url = base_url.format(page=page)
        response = requests.get(url, headers=headers)
        print(f"Fetching page {page}: Status code {response.status_code}")
        
        if response.status_code != 200:
            break  # Exit loop if the page does not exist or access is denied

        sel = Selector(text=response.text)
        image_urls = sel.xpath("//figure[contains(@class, 'ld-sp-img')]//img/@data-src").getall()
        titles = sel.xpath("//div[@class='ld-sp-info']/h3/a/text()").getall()

        if not image_urls and not titles:
            # Stop if no products are found (indicating the last page has been reached)
            print("No more products found. Exiting pagination.")
            break
        
        # Combine the products for the current page
        products = [{"image_url": img, "title": title} for img, title in zip(image_urls, titles)]
        all_products.extend(products)

        # Go to the next page
        page += 1

    # Cache the data
    with open(CACHE_FILE_FILESE, 'w') as f:
        json.dump({"timestamp": time.time(), "data": all_products}, f)

    return all_products



    
def get_cached_products():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            if time.time() - cache["timestamp"] < CACHE_EXPIRATION:
                return cache["data"]
    return fetch_and_cache_products()

def get_cached_fliese():
    if os.path.exists(CACHE_FILE_FILESE):
        with open(CACHE_FILE_FILESE, 'r') as f:
            cache = json.load(f)
            if time.time() - cache["timestamp"] < CACHE_EXPIRATION:
                return cache["data"]
    return fetch_and_cache_fliese()

def cache_updater():
    """ Background Thread to update cache every 15 minutes."""
    while True:
        print("Updating cache...")
        fetch_and_cache_products()
        time.sleep(CACHE_EXPIRATION)
@app.route("/")
def index():
    fliese_products = []
    glas_products = []
    if os.path.exists(CACHE_FILE_FILESE):
        with open(CACHE_FILE_FILESE, 'r') as f:
            cache = json.load(f)
            fliese_products = random.sample(cache["data"], 20)

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            glas_products = random.sample(cache["data"], 20)            
    return render_template('index.html',glas_products=glas_products,fliese_products=fliese_products)

@app.route("/category/<name>")
def category(name):
    if name == "glas": 
        products = get_cached_products()
    else:
        products = get_cached_fliese()
    return render_template('category.html', name=name,products=products)


if __name__ == "__main__":
    Thread(target=cache_updater, daemon=True).start()
    app.run(debug=True)