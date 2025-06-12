from django import forms
from .models import Mdfile

class CreateMdfileForm(forms.ModelForm):
    class Meta:
        model = Mdfile
        fields = ['title','base_text']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'ファイル名を入力'
            }),
            'base_text':  forms.Textarea(attrs={
                'class': 'full-height-textarea',
            })
        }

