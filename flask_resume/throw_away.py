from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    child = db.relationship("Child", backref = db.backref('parent', lazy = True, uselist = False))

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)


@app.route('/index', methods=('GET',))
@app.route('/', methods=('GET',))
def index(): 
    return 'This is a piece of throw-away code.'

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
    
    parent = Parent()
    db.session.add(parent)
    db.session.commit()
    print(hasattr(parent, 'child'))
    print(Parent.query.get(1).child_id)
    print(type(parent.child))

    child = Child()
    Parent.query.get(1).child = child
    db.session.add(child)
    db.session.commit()
    print("Parent instance has a child", hasattr(Parent.query.get(1), 'child'))
    print(Parent.query.get(1).child_id)
    print("Type of parent.child", type(Parent.query.get(1).child))
    print("Child instance has a parent", hasattr(child, 'parent'))
    print("Type of child.parent", type(child.parent))