from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

class New_Page(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextAreaField('Write Notes Here')
    image = FileField('Add an Image', validators=[FileAllowed(['jpg','jpeg', 'png'])])
    submit = SubmitField('Create Page')

class Edit_Page(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextAreaField('Write Notes Here')
    image = FileField('Add an Image', validators=[FileAllowed(['jpg','jpeg', 'png'])])
    submit = SubmitField('Edit Page')