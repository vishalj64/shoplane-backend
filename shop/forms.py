
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        fields = ["rate", "review"]
        model = models.Review


