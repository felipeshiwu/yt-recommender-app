from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class PredictForm(FlaskForm):
    predict_url = StringField('Put here a youtube video link')
    submit = SubmitField('Predict')