from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class SignUpForm(Form):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[Length(min=6)])
  email = StringField('Email', validators=[Email()])

class LogInForm(Form):
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[Length(min=6)])

# class EditForm(Form):
#   password = PasswordField('password', validators=[Length(min=6)])
#   email = StringField('Email', validators=[Email()])
#   bio = StringField('bio')
#   location = StringField('location')
#   image = StringField('image')

class TradeForm(Form):
  name = HiddenField('name')
  platform = HiddenField('platform')

class RateForm(Form):
  stars = HiddenField('stars')
  feedback = TextAreaField('feedback')

class BioForm(Form):
  bio = TextAreaField('bio')

class ImageForm(Form):
  img = StringField('image')

class DeleteForm(Form):
  own = HiddenField('own')
  name = HiddenField('name')
  platform = HiddenField('platform')

class EmailForm(Form):
  email = StringField('Email', validators=[Email()])

class LocationForm(Form):
  lat = HiddenField('lat', validators=[DataRequired()])
  lng = HiddenField('lng', validators=[DataRequired()])
  loc = HiddenField('loc', validators=[DataRequired()])