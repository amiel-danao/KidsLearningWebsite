# Generated by Django 4.1.5 on 2023-01-12 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_announcement_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnails/'),
        ),
    ]
