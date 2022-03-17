from django.db import models
from django import forms
# Create your models here.
# Create your models here.

class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128)
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput)


class User(models.Model):
    '''Users'''

    gender = (
        ('male'),
        ('female'),
    )

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = 'USERS'
        verbose_name_plural = 'USERS'