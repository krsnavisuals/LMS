from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(2, 255)])
    author = StringField('Author', validators=[DataRequired(), Length(2, 255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    section = SelectField('Section', validators=[DataRequired()])
    submit = SubmitField('Book Details')

class ReviewForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Review')

class SectionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Section')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
