from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateListForm(FlaskForm):
    name = StringField('List Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description (optional)', validators=[Length(max=200)])
    emoji = SelectField('Icon', 
                       choices=[
                           ('📚', '📚 Study'),
                           ('💪', '💪 Gym/Fitness'),
                           ('💼', '💼 Work'),
                           ('🏠', '🏠 Personal'),
                           ('🛒', '🛒 Shopping'),
                           ('💊', '💊 Health'),
                           ('🎯', '🎯 Goals'),
                           ('🎮', '🎮 Hobbies'),
                           ('📋', '📋 General')
                       ],
                       default='📋')
    color = SelectField('Color', 
                       choices=[
                           ('#2196F3', '🔵 Blue'),
                           ('#4CAF50', '🟢 Green'), 
                           ('#FF9800', '🟠 Orange'),
                           ('#9C27B0', '🟣 Purple'),
                           ('#F44336', '🔴 Red'),
                           ('#795548', '🟤 Brown'),
                           ('#607D8B', '⚫ Gray'),
                           ('#E91E63', '🌸 Pink'),
                           ('#00BCD4', '🔷 Cyan')
                       ],
                       default='#2196F3')
    submit = SubmitField('Create List')
