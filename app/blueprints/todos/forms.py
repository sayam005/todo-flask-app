from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeLocalField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class TodoForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Description (optional)', validators=[Length(max=200)])
    
    # List selection dropdown - NEW
    list_id = SelectField('Add to List', coerce=int, validators=[Optional()])
    
    # Scheduling - when do you want to do this task? - NEW
    scheduled_date = DateField('Schedule for Date (optional)', validators=[Optional()])
    
    # Category dropdown with custom option
    category = SelectField('Category', 
                          choices=[
                              ('daily', 'Daily (ends today)'),
                              ('weekly', 'Weekly (7 days)'),
                              ('monthly', 'Monthly (30 days)'),
                              ('custom', 'Custom deadline')
                          ],
                          default='daily')
    
    # Custom deadline field
    custom_deadline = DateTimeLocalField('Custom Deadline', 
                                        validators=[Optional()],
                                        format='%Y-%m-%dT%H:%M')
    
    submit = SubmitField('Add Task')
