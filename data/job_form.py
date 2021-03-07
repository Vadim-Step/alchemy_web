from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = TextField('Job Title', validators=[DataRequired()])
    tl_id = TextField('Team Leader id', validators=[DataRequired()])
    work_size = TextField('Work Size', validators=[DataRequired()])
    collaborators = TextField('Collaborators', validators=[DataRequired()])
    finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
