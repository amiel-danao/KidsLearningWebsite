# Generated by Django 4.1.5 on 2023-01-07 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='time',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
