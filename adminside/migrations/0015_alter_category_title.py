# Generated by Django 5.0.7 on 2024-08-17 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0014_remove_additional_images_image1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
