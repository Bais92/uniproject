# Generated by Django 2.2.9 on 2020-02-22 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fragebogen', '0007_auto_20200222_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='results',
            old_name='experiment',
            new_name='questionexperiment',
        ),
        migrations.RemoveField(
            model_name='results',
            name='question',
        ),
    ]