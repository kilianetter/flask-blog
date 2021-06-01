from flask_login import current_user
from blog.models import User

# flask_wtf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

### User ###
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('email', 
                            validators=[DataRequired(), Length(min=2, max=60), Email()])
    password = PasswordField('password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Sorry, this username is already taken!')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Sorry, this email is already in use!')


class LoginForm(FlaskForm):
    email = StringField('email', 
                            validators=[DataRequired(), Length(min=2, max=60), Email()])
    password = PasswordField('password',
                            validators=[DataRequired()])
    remember = BooleanField('stay logged in')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('email', 
                            validators=[DataRequired(), Length(min=2, max=60), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])                            
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Sorry, this username is already taken!')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Sorry, this email is already in use!')


### Password Reset ###
class RequestResetForm(FlaskForm):
    email = StringField('email', 
                            validators=[DataRequired(), Length(min=2, max=60), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Invalid Email! Are you sure, you have an account?')
            

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])    
    submit = SubmitField('Reset Password')