from django.db import models
import uuid

def generate_id(length=8):
    import string, random
    chars = string.ascii_letters + string.digits
    while True:
        new_id = ''.join(random.choices(chars, k=length))
        if not Mdfile.objects.filter(id=new_id).exists():
            return new_id

class Share(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        unique=True,
        default=generate_id,
        editable=False
    )
    file = models.ForeignKey(
        "mdapp.Mdfile",
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE
    )

# Create your models here.
class Mdfile(models.Model):
    class Meta:
        db_table = 'mdfiles'

    id = models.CharField(
        primary_key=True,
        max_length=20,
        unique=True,
        default=generate_id,
        editable=False
    )
    title = models.CharField(verbose_name='ファイル名', max_length=100)
    base_text = models.TextField(verbose_name='文書データ')
    html_text = models.TextField(verbose_name='htmlデータ')
    url = models.CharField(verbose_name='pdfurl', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now_add=True)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE
    )

    # 同じユーザで同じタイトルを許さない
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_title_per_user')
        ]

    def __str__(self):
        return super().__str__()