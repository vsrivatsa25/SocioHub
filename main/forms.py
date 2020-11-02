from datetime import timedelta
from .models import Post, ProfilePic, UserInterests, Like, Comment
from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'img','topic','location']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['img']

class InterestForm(forms.ModelForm):
    class Meta:
        model = UserInterests
        fields = ['interest']

class LikeSubmit(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post']

class CommentSubmit(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','post']
