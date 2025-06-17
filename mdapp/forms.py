from django import forms
from .models import Mdfile, Share
from accounts.models import User
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

class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ['to_user']
    # 'to_user' という名前のフィールドを定義
    to_user = forms.ModelChoiceField(
        queryset=User.objects.all(), # データベースからすべてのユーザーを取得
        label="シェアするユーザー",    # フォームに表示されるラベル
        empty_label="ユーザーを選択してください", # 選択されていない場合のデフォルト表示
        # required=True, # デフォルトでTrue。選択必須にするなら明示的に書いても良い
    )

    def clean_to_user(self):
        to_user = self.cleaned_data['to_user']
        if (self.sharer == to_user):
            return ValidationError('自分は選択できません')
        return to_user

    def __init__(self, *args, **kwargs):
        # フォームを初期化する際に、自分自身（シェアする側）をquerysetから除外したい場合
        sharer = kwargs.pop('sharer', None)
        super().__init__(*args, **kwargs)
        self.sharer = sharer
        if sharer:
            # 現在のユーザーを除外したユーザーのクエリセットを設定
            self.fields['to_user'].queryset = User.objects.exclude(pk=sharer.pk)
        else:
            # sharer が提供されなかった場合は、すべてのユーザーを表示する（またはエラー処理）
            self.fields['to_user'].queryset = User.objects.all()
