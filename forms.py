from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import TextAreaField


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(3, 30)])
    bio = TextAreaField("Bio",       validators=[Length(max=250)])
    avatar = FileField("New Avatar (optional)")
    banner = FileField("New Banner (optional)")
    submit = SubmitField("Save changes")


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(3, 30)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(6, 64)])
    confirm = PasswordField("Confirm",
                            validators=[DataRequired(), EqualTo("password")])
    banner = FileField("Profile Banner (optional)")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email",     validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
