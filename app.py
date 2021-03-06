from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_bcrypt import Bcrypt
import os
from forms import SignUpForm, LogInForm, TradeForm, RateForm, BioForm, ImageForm, DeleteForm, EmailForm, LocationForm
from flask_wtf import CsrfProtect
import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from models.shared import db
import re

app = Flask(__name__)
app.url_map.strict_slashes = False
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL', 'postgres://localhost/game_exchange')
# app.config['SQLALCHEMY_DATABASE_URI']='postgres://localhost/game_exchange'

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
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)


    def __init__(self, username, password, email, date_joined, bio=None, location="San Francisco, CA", image="../static/images/crash.jpg", cred=0, lat=37.7749, lng= -122.4194):
     self.username =username
     self.password = bcrypt.generate_password_hash(password).decode('utf-8')
     self.email = email
     self.date_joined = date_joined
     self.bio = bio
     self.location = location
     self.image = image
     self.cred = cred
     self.lat = lat
     self.lng = lng

from models.games import Game
from models.rating import Rating

user_games = db.Table('user_games', 
  db.Column('id', db.Integer, primary_key=True),
  db.Column('game_id', db.Integer, db.ForeignKey('games.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
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

@app.route('/users/<int:id>/editimg', methods=['POST'])
@login_required
def editimg(id):
  user = User.query.get(session['user_id'])
  imgForm = ImageForm()
  imgForm.img.default = "../static/images/crash.jpg"
  if (imgForm.img.data != imgForm.img.default):
    if (imgForm.img.data == ""):
      user.image = imgForm.img.default
      db.session.commit()
      flash('Image Successfully Updated')
      return redirect(url_for('show', id=user.id))
    user.image = imgForm.img.data
    db.session.commit()
    flash('Image Successfully Updated')
    return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>/editbio', methods=['POST'])
@login_required
def editbio(id):
  user = User.query.get(session['user_id'])
  bioForm = BioForm()
  bioForm.bio.default = user.bio
  if (bioForm.bio.data != bioForm.bio.default):
    user.bio = bioForm.bio.data
    db.session.commit()
    flash('Bio Successfully Updated')
    return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>/editemail', methods=['POST'])
@login_required
def editemail(id):
  user = User.query.get(session['user_id'])
  emailForm = EmailForm()
  emailForm.email.default = user.email
  if emailForm.validate_on_submit():
    if (emailForm.email.data != emailForm.email.default):
      users1 = user.query.all()
      for user1 in users1:
        if (emailForm.email.data == user1.email):
          flash('Error: Email is already in use by another user')
          return redirect(url_for('show', id=user.id))
      user.email = emailForm.email.data
      db.session.commit()
      flash('Email Successfully Updated')
      return redirect(url_for('show', id=user.id))
    flash('Your original email, '+user.email+' has been saved')
    return redirect(url_for('show', id=user.id))
  flash('Error: Invalid Email Address')
  return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>/editlocation', methods=['POST'])
@login_required
def editlocation(id):
  user = User.query.get(session['user_id'])
  locationForm = LocationForm()
  if locationForm.validate_on_submit():
    user.lat = locationForm.lat.data
    user.lng = locationForm.lng.data
    user.location = locationForm.loc.data
    db.session.commit()
    flash('Location Sucessfully Updated')
    return redirect(url_for('show', id=user.id))
  flash('Previous Location Saved')
  return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>/deletegame', methods=['POST'])
@login_required
def deletegame(id):
  user = User.query.get(session['user_id'])
  delForm = DeleteForm()
  delForm.own.data = (delForm.own.data == 'True')
  findGame = user.games.all()
  for game in findGame:
    if game.name == delForm.name.data and game.platform == delForm.platform.data and game.own == delForm.own.data:
      db.session.delete(game)
      db.session.commit()
      flash('Successfully Deleted ' + game.name)
  return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>', methods=['POST'])
@login_required
def trade(id):
  user = User.query.get(session['user_id'])
  form = TradeForm()
  user2 = User.query.get(id)
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
  new_rating=Rating(giv_id=id, rec_id=id2, stars=int(form.stars.data), feedback=form.feedback.data)
  db.session.add(new_rating)
  db.session.commit()
  return redirect(url_for('show', id=user.id))

@app.route('/users/<int:id>')
@login_required
def show(id):
  user = User.query.get(int(session['user_id']))
  print('biooooo', user)
  form = TradeForm()
  delForm = DeleteForm()
  bioForm = BioForm()
  imgForm = ImageForm()
  emailForm = EmailForm()
  locationForm = LocationForm()
  r='Not Rated'
  try:
    user2 = User.query.get(id)
  except:
    user2 = None
  print(user2)
  if (user2==None):
    return render_template('errors/user.html', user=user)
  # from IPython import embed; embed()
  ratings = Rating.query.all()
  user_rating = []
  for rating in ratings:
    if rating.rec_id == id:
      user_rating.append(rating.stars)
  if (len(user_rating) > 0):
    r = round(sum(user_rating)/len(user_rating), 2)
  games = Game.query.all()
  return render_template('users/show.html',user=user, user2=user2, games=games, form=form, r=r, bioForm=bioForm, imgForm=imgForm, delForm=delForm, emailForm=emailForm, locationForm=locationForm)

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
    flash('Successfully Added '+new_game.name)
    return render_template('search.html', user=user)

@app.errorhandler(404)
def page_not_found(err):
    user = User.query.get(int(session['user_id']))
    return render_template('errors/404.html', user=user), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    # host = int(os.environ.get("HOST", '127.0.0.1'))
    app.run(host='0.0.0.0', port=port)






