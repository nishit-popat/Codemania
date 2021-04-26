''' This is form file
    This file contains different forms required in project
    Author : Nishit Popat '''

from .models import Snippet
from django import forms
from django_ace import AceWidget

#Snippet form which will have one textarea in the form of ace widget
class SnippetForm(forms.ModelForm):
    class Meta:
        #Snippet model is used for creating this form
        model = Snippet
        #Different attributes for ace widget
        widgets = {
            "text": AceWidget(mode='c_cpp', theme='twilight',width="100%",
        height="500px", fontsize="14px"),
        }
        exclude = ()
