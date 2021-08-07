from market import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), unique=False, nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100000)
    items = db.relationship('Cryptocurrency', backref='owned_user', lazy=True) #relacja
    # Iphone(item).backref(owned_user) -> daje nam usera
    #lazy = True bo tak


class Cryptocurrency(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    shortcut = db.Column(db.String(length=5), nullable=False, unique=True)
    price = db.Column(db.Float(), nullable=False, unique=False)
    percent24hours = db.Column(db.Float(), nullable=True, unique=False, default=0.0)
    percent7days = db.Column(db.Float(), nullable=True, unique=False, default=0.0)
    market_cap = db.Column(db.Float(), nullable=True, unique=False, default=0.0)
    volume24h = db.Column(db.Float(), nullable=True, unique=False, default=0.0)
    circulating_supply = db.Column(db.Float(), nullable=True, unique=False, default=0.0)
    owned = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.name}({self.shortcut})'
