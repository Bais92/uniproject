# Generated by Django 2.2.9 on 2020-02-21 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fragebogen', '0004_nudge'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fragebogen.Question'),
        ),
    ]
