from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    createdOn = db.Column(db.DateTime, default=datetime.now())
    updatedOn = db.Column(db.DateTime)
    completion_status= db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"Task( id = {self.id} , title = {self.title}, completion_status = {self.completion_status} )"

#db.create_all()
