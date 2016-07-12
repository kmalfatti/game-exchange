from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_bcrypt import Bcrypt
from models.shared import db
# from models.users import User
import os
from forms import SignUpForm, LogInForm, EditForm
from flask_wtf import CsrfProtect
from functools import wraps
import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user



app = Flask(__name__)
app.url_map.strict_slashes = False
bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/game_exchange'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False

db.init_app(app)
with app.app_context():
    db.create_all()

CsrfProtect(app)


# TODO set up secret key
# os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'random'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    bio = db.Column(db.Text())
    location = db.Column(db.Text())
    image = db.Column(db.Text())
    cred = db.Column(db.Integer)
    games = db.relationship('Game', backref='user', lazy='dynamic')
    ratings = db.relationship('Rating', backref='rating', lazy='dynamic')


    def __init__(self, username, password, email, date_joined, bio=None, location=None, image=None, cred=None):
     self.username =username
     self.password = bcrypt.generate_password_hash(password).decode('utf-8')
     self.email = email
     self.date_joined = date_joined
     self.bio = bio
     self.location = location
     self.image = image
     self.cred = cred

from models.games import Game
from models.rating import Rating

# user_games = db.Table('user_games', 
#   db.Column('id', db.Integer, primary_key=True),
#   db.Column('game_id', db.Integer, db.ForeignKey('games.id')),
#   db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
# )

# user_rating = db.Table('user_ratings',
#   db.Column('id', db.Integer, primary_key=True),
#   db.Column('receiver_id', db.Integer, db.ForeignKey('ratings.rec_id')),
# )


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/search')
def search():
  return render_template('search.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/signup')
def signup():
  form = SignUpForm()
  return render_template('signup.html', form=form)

@app.route('/users', methods=['POST'])
def create():
  form = SignUpForm()
  error = None
  if form.validate_on_submit():
    new_user=User(form.username.data, form.password.data, form.email.data, datetime.datetime.now().date())  
    db.session.add(new_user)
    db.session.commit()
    id = User.query.get(new_user.id).id
    flash('Success!')
    return redirect(url_for('show', id=id))
  return render_template('signup.html', form=form, error=error)

@app.route('/users')
def user_index():
  print('teeeeeeest')
  return render_template('users/index.html', users=User.query.all())


@app.route('/users/<int:id>')
def show(id):
  print(id)
  user = User.query.get(id)
  print(user)
  return render_template('users/show.html', user=user)


@app.route('/users/<int:id>/edit')
def edit(id):
  form = EditForm()
  return render_template('users/edit.html', form=form)



if __name__ == '__main__':
    app.run(debug=True, port=3000)