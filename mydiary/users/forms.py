from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from mydiary.models import User
from flask import session

class RegisterationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    c_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    dp = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    register = SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email Already Taken. Please Try a different one.')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError('User Name Already Taken. Please Try a different one.')
 

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    change_dp = FileField('Change Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    old_password = PasswordField('Old Password')
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Save Changes')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('This email has not been found')

class AccountActivationForm(FlaskForm):
    code = StringField('Activation Code', validators=[DataRequired()])
    submit = SubmitField('Activate Account')