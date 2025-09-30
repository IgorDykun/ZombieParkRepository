from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default="user")


    tickets = db.relationship("Ticket", backref="owner", lazy=True)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # дата відвідування
    ticket_type = db.Column(db.String(50), nullable=False, default="standard")   # тип: standard / vip
    price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
