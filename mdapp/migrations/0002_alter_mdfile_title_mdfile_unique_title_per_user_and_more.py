# Generated by Django 5.2.3 on 2025-06-15 07:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdfile',
            name='title',
            field=models.CharField(max_length=100, verbose_name='ファイル名'),
        ),
        migrations.AddConstraint(
            model_name='mdfile',
            constraint=models.UniqueConstraint(fields=('user', 'title'), name='unique_title_per_user'),
        ),
        migrations.AlterModelTable(
            name='mdfile',
            table=None,
        ),
    ]
