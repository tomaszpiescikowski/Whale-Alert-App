from market import db, bcrypt
from market.decorations import better_numbers_template


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), unique=False, nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100000)
    items = db.relationship('Cryptocurrency', backref='owned_user', lazy=True)  # relacja

    # Iphone(item).backref(owned_user) -> daje nam usera
    # lazy = True bo tak

    @property  # individual to an instance
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def __repr__(self):
        return f'#{self.id}: {self.username}'


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

    @property
    def pretty_market_cap(self):
        return better_numbers_template(self.market_cap)

    @property
    def pretty_volume24h(self):
        return better_numbers_template(self.volume24h)

    @property
    def pretty_circulating_supply(self):
        return better_numbers_template(self.circulating_supply)

    @property
    def pretty_price(self):
        return better_numbers_template(self.price)
