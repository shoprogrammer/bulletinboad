from django import forms
from .models import BoardModel,Comment,Favorite,Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class BoardForm(forms.ModelForm):
    class Meta:
        model = BoardModel
        fields = ['title','content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text="emailアドレスは必須です.")

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['board']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['title','message','email']