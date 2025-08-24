"""
Backend : Modèles DB (Prochaine étape, toi qui codes) :

Deux models : User (id, username, password_hash) et
            Idea (id, title, description, tags, user_id, timestamp).

Utilise SQLite pour l'MVP (facile, no setup server).
"""
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    ideas = db.relationship('Idea', backref='author', lazy=True)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(200))  # e.g., "video,funny"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)