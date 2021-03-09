from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField
from wtforms.validators import DataRequired


class DepForm(FlaskForm):
    title = TextField('Dep Title', validators=[DataRequired()])
    chief = TextField('Chief id', validators=[DataRequired()])
    members = TextField('Members', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
