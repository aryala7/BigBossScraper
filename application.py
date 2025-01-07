# app.py
from flask import Flask, render_template
from threading import Thread
from cache_manager import get_cached_products, get_cached_fliese, CACHE_EXPIRATION, fetch_and_cache_products
import os
import json
import random
import time

app = Flask(__name__)

@app.route("/")
def index():
    fliese_products = []
    glas_products = []

    if os.path.exists(get_cached_fliese.cache_file):
        with open(get_cached_fliese.cache_file, 'r') as f:
            cache = json.load(f)
            fliese_products = random.sample(cache["data"], 20)

    if os.path.exists(get_cached_products.cache_file):
        with open(get_cached_products.cache_file, 'r') as f:
            cache = json.load(f)
            glas_products = random.sample(cache["data"], 20)

    return render_template('index.html', glas_products=glas_products, fliese_products=fliese_products)

@app.route("/category/<name>")
def category(name):
    if name == "glas":
        products = get_cached_products()
    else:
        products = get_cached_fliese()

    return render_template('category.html', name=name, products=products)

def cache_updater():
    """ Background Thread to update cache every 15 minutes."""
    while True:
        print("Updating cache...")
        fetch_and_cache_products()
        time.sleep(CACHE_EXPIRATION)

if __name__ == "__main__":
    Thread(target=cache_updater, daemon=True).start()
    app.run(debug=True)
