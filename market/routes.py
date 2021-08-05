from market import app
from market.models import Cryptocurrency
from market.scraper import generate_json, read_from_json
from flask import render_template


@app.route('/')
def root_page():
    generate_json()
    read_from_json()
    cryptos = Cryptocurrency.query.all()
    return render_template('base.html', cryptos=cryptos)