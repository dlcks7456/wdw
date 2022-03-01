from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class Questions(FlaskForm) :
    age = IntegerField("나이", validators=[NumberRange(0, 100)])