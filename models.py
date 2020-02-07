from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

from dbconfig import db

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
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'User ' + str(self.id)