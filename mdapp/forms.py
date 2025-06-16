from django import forms
from .models import Mdfile
from django.core.exceptions import ValidationError

class CreateMdfileForm(forms.ModelForm):
    class Meta:
        model = Mdfile
        fields = ['title','base_text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-title',
                'placeholder': 'ファイル名を入力'
            }),
            'base_text':  forms.Textarea(attrs={
                'id': 'auto-textarea',
                'class': 'form-base_text',
            })
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # ← 必須
        super().__init__(*args, **kwargs)
    def clean_title(self):
        title = self.cleaned_data['title']
        if Mdfile.objects.filter(user=self.user, title=title).exists():
            if self.instance.pk:
                # 既存のインスタンスで、タイトルが変更されていない場合はエラーを出さない
                if self.instance.title == title:
                    return title
            raise ValidationError('このファイル名は既に使われています。')
        return title

