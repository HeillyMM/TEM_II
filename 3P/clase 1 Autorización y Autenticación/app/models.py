from flask_login import UserMixin
from app.extensions import db

class User(db.Model,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String(20),default="user")

    def get_id(self):
        return str(self.id)