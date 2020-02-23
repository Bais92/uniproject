# Generated by Django 2.2.9 on 2020-02-21 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fragebogen', '0003_auto_20200221_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nudge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('nudge_type', models.CharField(max_length=32)),
                ('presentation_type', models.CharField(choices=[('Kein', 'Kein'), ('Falsch', 'Falsch'), ('Richtig', 'Richtig')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]