# Generated by Django 5.2.3 on 2025-06-16 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdapp', '0004_alter_mdfile_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mdfile',
            old_name='author',
            new_name='url',
        ),
    ]
