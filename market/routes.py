from market import app
from market.models import Cryptocurrency
from market.scraper import generate_json, read_from_json
from market.mailer import send_email
from flask import render_template, request, url_for, redirect
from market.forms import RegisterForm

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard_page():
    generate_json()
    read_from_json()
    cryptos = Cryptocurrency.query.all()
    return render_template('base.html', cryptos=cryptos)


@app.route('/whale', methods=['POST', 'GET'])
def whale_page():
    if request.method == "POST":
        email = str(request.form['email'])
        password = str(request.form['password'])
        password_good = "eloelo123"
        if password == password_good:
            send_email(email, password)
            print("SENDING EMAIL")
        else:
            print("BAD PASSWORD:", email, password)
    return render_template('whale.html')
