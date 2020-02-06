from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Resume(db.Model):
    '''
    self.id : int
    self.user : User
    '''
    id = db.Column(db.Integer, primary_key = True)
    placeHolder = db.Column(db.Text, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref = db.backref('resume', lazy = True, uselist = False))

    def __repr__(self):
        return 'Resume ' + str(self.id)
class User(db.Model):
    '''
    self.id : int
    self.userName : str
    self.credentials : str
    self.resume : Resume
    '''
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(100), nullable = False)
    credentials = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return 'User ' + str(self.id)