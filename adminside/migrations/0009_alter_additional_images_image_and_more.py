# Generated by Django 5.0.7 on 2024-08-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0008_offers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional_images',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='additional_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='Featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='featured_images/'),
        ),
    ]
