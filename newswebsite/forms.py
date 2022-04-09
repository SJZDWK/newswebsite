from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def words_validator(comment):
    if len(comment)<5:
        raise ValidationError("Too short comment, please write at least 5 characters! ")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(),validators=[words_validator])

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'id'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if User.objects.filter(username=username):
           raise forms.ValidationError("Exist user!")
        if User.objects.filter(email=email):
           raise forms.ValidationError("Exist email!")

        try:
           validate_email(email)
        except ValidationError:
           raise forms.ValidationError("Error of email format!")

        if len(password) < 6:
           raise forms.ValidationError("Password should be at least 6 characters! ")

        if password_confirm != password:
           raise forms.ValidationError("The two passwords you typed do not match!")

class EditForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}),required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}),required=False)
    avatar = forms.FileField(label="upload avatar")

    def clean(self):
        cleaned_data = super(EditForm,self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")


        try:
           validate_email(email)
        except ValidationError:
           raise forms.ValidationError("Error of email format!")

        if len(password) < 6:
           raise forms.ValidationError("Password should be at least 6 characters! ")

        if password_confirm != password:
           raise forms.ValidationError("The two passwords you typed do not match!")
