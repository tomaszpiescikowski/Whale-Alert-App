from market import db


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

    def __repr__(self):
        return f'{self.name}({self.shortcut})'