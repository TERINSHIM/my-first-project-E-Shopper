# Generated by Django 5.0.7 on 2024-08-17 07:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0010_rename_image_additional_images_image1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additional_information',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='additional_info',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='additional_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='additional_images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='additional_images/'),
        ),
        migrations.DeleteModel(
            name='additional_images',
        ),
        migrations.DeleteModel(
            name='additional_information',
        ),
    ]
