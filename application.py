import os
import json
import time
from threading import Thread
from flask import Flask,render_template
from scrapy import Selector
import requests
app = Flask(__name__)

CACHE_FILE = "products.json"
CACHE_EXPIRATION = 60 * 15 #15 minutes 

def fetch_and_cache_products():
    url = "https://sahandjam.com/page/1/?s&post_type=product"
    response = requests.get(url)
    
    print(response.status_code , 'aklsjdjaskd')
    if response.status_code == 200:
        print("2222")
        sel = Selector(text=response.text)
        image_urls = sel.xpath("//div[@class='image_box']/img/@src").getall()
        print(image_urls)
        print("asjkdajlksd")
        titles = sel.xpath('//div[@class="content_box"]/h2/a/text()').getall()
        scraped_data = [{"image_url": img, "title": title} for img, title in zip(image_urls, titles)]
        with open(CACHE_FILE, 'w') as f:
           json.dump({"timestamp": time.time(),"data": scraped_data}, f)
        return scraped_data
    
def get_cached_products():
    # if os.path.exists(CACHE_FILE):
    #     print("here")
    #     with open(CACHE_FILE, 'r') as f:
    #         cache = json.load(f)
    #         if time.time() - cache["timestamp"] < CACHE_EXPIRATION:
    #             return cache["data"]
    return fetch_and_cache_products()

def cache_updater():
    """ Background Thread to update cache every 15 minutes."""
    while True:
        print("Updating cache...")
        fetch_and_cache_products()
        time.sleep(CACHE_EXPIRATION)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/category/<name>")
def category(name):
    products = get_cached_products()
    return render_template('category.html', name=name,products=products)


if __name__ == "__main__":
    # Thread(target=cache_updater, daemon=True).start()
    app.run(debug=True)