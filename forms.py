from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import TextAreaField, StringField, SubmitField, SelectField, FileField


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

    banner = FileField("Profile Banner (optional)")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddGameForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[
                              DataRequired(), Length(max=250)])
    cover = FileField(
        "Cover (jpg/png)", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    background_image = FileField("Background Image", validators=[
                                 FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    torrent_file = FileField("Torrent File", validators=[
                             FileRequired(), FileAllowed(['torrent'])])
    category = SelectField("Category", coerce=int)   # dropdown
    submit = SubmitField("Add")
