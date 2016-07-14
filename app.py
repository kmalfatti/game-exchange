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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
CsrfProtect(app)

class User(db.Model, UserMixin):
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


    def __init__(self, username, password, email, date_joined, bio=None, location=None, image="../static/images/crash.jpg", cred=0):
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
@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.id == int(user_id)).first()
    # from IPython import embed; embed()
    return user


@app.route('/')
def index():
  # from IPython import embed; embed()
  try:
    user = User.query.get(int(session['user_id']))
  except:
    user = None
  return render_template('index.html', user=user)

@app.route('/about')
def about():
  try:
    user = User.query.get(int(session['user_id']))
  except:
    user = None
  return render_template('about.html', user=user)

@app.route('/search')
def search():
  try:
    user = User.query.get(int(session['user_id']))
  except:
    user = None
  return render_template('search.html', user=user)

@app.route('/contact')
def contact():
  try:
    user = User.query.get(int(session['user_id']))
  except:
    user = None
  return render_template('contact.html', user=user)

@app.route('/signup')
def signup():
  form = SignUpForm()
  return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LogInForm()
  error = None
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(username=request.form['username']).first()
      if user:
        is_authenticated = bcrypt.check_password_hash(user.password, form.password.data)
        if is_authenticated:
          flash('Logged in successfully.')
          login_user(user)
          session['logged_in'] = True
          return redirect(url_for('show', id=user.id))
        else:
          error = "Invalid Username/Password"
      else:
        error = "Invalid Username/Password"
  return render_template('login.html', form=form, error=error)

@app.route('/users', methods=['POST'])
def create():
  form = SignUpForm()
  error = None
  if form.validate_on_submit():
    new_user=User(form.username.data, form.password.data, form.email.data, datetime.datetime.now().date())  
    db.session.add(new_user)
    db.session.commit()
    id = User.query.get(new_user.id).id
    login_user(new_user)
    session['logged_in'] = True
    flash('Account successfully created!')
    return redirect(url_for('show', id=id))
  return render_template('signup.html', form=form, error=error)

@app.route('/users')
def user_index():
  return render_template('users/index.html', users=User.query.all())


@app.route('/users/<int:id>')
@login_required
def show(id):
  print(id)
  user = User.query.get(id)
  print(user)
  return render_template('users/show.html', user=user)


@app.route('/users/<int:id>/edit')
def edit(id):
  form = EditForm()
  return render_template('users/edit.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('Logged out')
    return redirect(url_for('login'))
    

if __name__ == '__main__':
    app.run(debug=True, port=3000)