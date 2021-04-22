from .models import Snippet
from django import forms
from django_ace import AceWidget


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        widgets = {
            "text": AceWidget(mode='c_cpp', theme='twilight',width="100%",
        height="500px", fontsize="14px"),
        }
        exclude = ()
