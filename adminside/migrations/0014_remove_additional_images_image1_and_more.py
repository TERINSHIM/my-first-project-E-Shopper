# Generated by Django 5.0.7 on 2024-08-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0013_remove_product_additional_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additional_images',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='additional_images',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='additional_images',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='additional_information',
            name='additional_info',
        ),
        migrations.AddField(
            model_name='additional_images',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='additional_information',
            name='spec',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='additional_information',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
