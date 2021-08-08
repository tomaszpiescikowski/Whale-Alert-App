from market import app, db
from market.models import Cryptocurrency, User
from market.scraper import generate_json, read_from_json
from market.mailer import send_email
from flask import render_template, request, url_for, redirect
from market.forms import RegisterForm


@app.route('/register', methods=['post', 'get'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password1.data,
                              )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('dashboard_page'))
    if form.errors is not {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')


    return render_template('register.html', form=form)


@app.route('/')
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
