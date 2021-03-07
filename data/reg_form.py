from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, TextField, IntegerField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    id = IntegerField('id', validators=[DataRequired()])
    surname = TextField('surname', validators=[DataRequired()])
    name = TextField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')
