from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TodoForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = StringField('Description (optional)', validators=[Length(max=200)])
    category = StringField('Category', validators=[DataRequired()], default='daily')
    submit = SubmitField('Add Task')
