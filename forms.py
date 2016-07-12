from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class SignUpForm(Form):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[Length(min=6)])
  email = StringField('Email', validators=[Email()])

class LogInForm(Form):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[Length(min=6)])

class EditForm(Form):
  password = PasswordField('password', validators=[Length(min=6)])
  email = StringField('Email', validators=[Email()])
  bio = StringField('bio')
  location = StringField('location')
  image = StringField('image')

  

