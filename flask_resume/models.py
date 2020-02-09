from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

from flask_resume import db

class Resume(db.Model):
    '''
    self.id : int
    self.user : User
    '''
    id = db.Column(db.Integer, primary_key = True)

    basic_info_id = db.Column(db.Integer, db.ForeignKey('basic_info.id'), nullable = False, default = -1)
    basic_info = db.relationship('Basic_info', backref = db.backref('resume', lazy = True, uselist = False))

    def __repr__(self):
        return 'Resume ' + str(self.id)

class Basic_info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    nation = db.Column(db.String(100), nullable = False)
    region = db.Column(db.String(100), nullable = False)
    birth = db.Column(db.Date, nullable = False)
    portrait_URL = db.Column(db.String(100), nullable = False)

class User(UserMixin, db.Model):
    '''
    self.id : int
    self.userName : str
    self.credentials : str
    self.resume : Resume
    '''
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)

    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable = False, default = -1)
    resume = db.relationship('Resume', backref = db.backref('user', lazy = True, uselist = False))
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'User ' + str(self.id)