from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_bcrypt import Bcrypt
import os
from forms import SignUpForm, LogInForm, EditForm, TradeForm, RateForm
from flask_wtf import CsrfProtect
import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from models.shared import db
import re

app = Flask(__name__)
app.url_map.strict_slashes = False
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://localhost/game_exchange')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/game_exchange'

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

# TODO - Refactor database design
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
    games = db.relationship('Game', backref='users', lazy='dynamic')
    ratings = db.relationship('Rating', backref='rating', lazy='dynamic')


    def __init__(self, username, password, email, date_joined, bio=None, location="San Francisco, CA", image="../static/images/crash.jpg", cred=0):
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

user_games = db.Table('user_games', 
  db.Column('id', db.Integer, primary_key=True),
  db.Column('game_id', db.Integer, db.ForeignKey('games.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

user_rating = db.Table('user_ratings',
  db.Column('id', db.Integer, primary_key=True),
  db.Column('rec_id', db.Integer, db.ForeignKey('ratings.rec_id')),
)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.id == int(user_id)).first()
    return user

@app.route('/')
def index():
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
          flash('Welcome back, '+user.username+'!')
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
@login_required
def user_index():
  user = User.query.get(int(session['user_id']))
  user_games = user.games.all()
  games = Game.query.all()
  return render_template('users/index.html', user=user, user_games=user_games, games=games)

@app.route('/users/<int:id>', methods=['POST'])
@login_required
def trade(id):
  form = TradeForm()
  print('id', id)
  user2 = User.query.get(id)
  print('user2 username', user2.username)
  user = User.query.get(session['user_id'])
  findGame = user.games.all()
  foundGame = []
  for game in findGame:
    if game.name == form.name.data and game.platform == form.platform.data:
      print('GAME', game.user_id)
      if (game.user_id == user.id) and (game.own==True):
        flash('You cannot trade games with yourself.')
        break
      foundGame.append(game)
      break
  if (len(foundGame) > 0):
    db.session.delete(foundGame[0])
    user.cred+=1
    db.session.commit()
    flash('Game traded!')
    return redirect(url_for('rate', id=user.id, id2=user2.id))
  else:
    flash('Error')
  return redirect(url_for('show', id=user.id, form=form, user2=user2))

@app.route('/users/<int:id>/rate/<int:id2>')
@login_required
def rate(id, id2):
  form = RateForm()
  user = User.query.get(id)
  user2 = User.query.get(id2)
  return render_template('users/rate.html', user=user, user2=user2, form=form)

@app.route('/users/<int:id>/rate/<int:id2>', methods=['POST'])
@login_required
def submit_rating(id, id2):
  form=RateForm()
  user = User.query.get(id)
  if(form.stars.data==''):
    flash("Click on a star to rate the user")
    return redirect(url_for('rate', id=id, id2=id2))
  if (id == id2):
    flash('Nice try...You should get 1 star for that! :(')
    return redirect(url_for('show', id=user.id))
  flash('Thank you!')
  new_rating=Rating(giv_id=id, rec_id=id2, stars=int(form.stars.data))
  db.session.add(new_rating)
  db.session.commit()
  return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>')
@login_required
def show(id):
  form = TradeForm()
  rateForm = RateForm()
  r='Not Rated'
  user2 = User.query.get(id)
  user = User.query.get(int(session['user_id']))
  ratings = Rating.query.all()
  user_rating = []
  for rating in ratings:
    if rating.rec_id == id:
      user_rating.append(rating.stars)
  if (len(user_rating) > 0):
    r = round(sum(user_rating)/len(user_rating), 2)
  games = Game.query.all()
  return render_template('users/show.html',user=user, user2=user2, games=games, form=form, rateForm=rateForm, r=r)

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

@app.route('/search', methods=['POST'])
@login_required
def add_game():
    user = User.query.get(int(session['user_id']))
    game_id = request.form['game_id']
    if request.form['action'] == 'I own it!':
      own = True
      user.games_owned = game_id 
    else:
      own = False
      user.games_wanted = game_id
    name = request.form['name']
    platform = re.sub('-',' ', request.form['platform'])
    cover = request.form['image']
    new_game = Game(name, user.id, game_id, cover, own, platform)
    db.session.add(new_game)
    db.session.commit()
    flash('Successfully Added Game')
    return render_template('search.html', user=user)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    # print(port)
    # host = int(os.environ.get("HOST", '127.0.0.1'))
    app.run(host='0.0.0.0', port=port)






