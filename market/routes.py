from market import app, db
from market.models import Cryptocurrency, User
from market.scraper import generate_json, read_from_json
from market.mailer import send_email
from flask import render_template, request, url_for, redirect, flash, get_flashed_messages
from market.forms import RegisterForm


@app.route('/signup', methods=['post', 'get'])
def signup_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data,
                              )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('dashboard_page'))
    if form.errors is not {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')


    return render_template('signup.html', form=form)


@app.route('/')
def root_page():
    return render_template('root.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard_page():
    generate_json()
    read_from_json()
    cryptos = Cryptocurrency.query.all()
    return render_template('dashboard.html', cryptos=cryptos)


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
