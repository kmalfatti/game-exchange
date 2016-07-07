from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from forms import SignUpForm, LogInForm
from flask_wtf import CsrfProtect
from functools import wraps
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user



app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/game_exchange'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CsrfProtect(app)

# TODO set up secret key
# os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'random'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False, unique=True)
    email = db.Column(db.Text(), nullable=False, unique=True)

    def __init__(self, username, password, email):
     self.username =username
     self.password = bcrypt.generate_password_hash(password).decode('utf-8')
     self.email = email




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
    new_user=User(form.username.data, form.password.data, form.email.data)
    db.session.add(new_user)
    db.session.commit()
    flash('Success!')
    return redirect(url_for('users/<int:id>'))
  return render_template('signup.html', form=form, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=3000)