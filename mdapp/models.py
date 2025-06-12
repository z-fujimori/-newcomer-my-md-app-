from django.db import models

# Create your models here.
class Mdfile(models.Model):
    class Meta:
        db_table = 'mdfiles'

    title = models.CharField(verbose_name='ファイル名', max_length=100,unique=True)
    base_text = models.TextField(verbose_name='文書データ')
    html_text = models.TextField(verbose_name='htmlデータ')
    author = models.CharField(verbose_name='pdfurl', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now_add=True)

    def __str__(self):
        return super().__str__()