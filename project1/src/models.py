from django.db import models
from django import forms
from django.contrib.auth.models import User
import os


class Image(models.Model):
    name = models.CharField(max_length=250)
    file = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return os.path.basename(self.file.name)

class ImageForm(forms.Form):
    name = forms.CharField()
    file = forms.ImageField()
    