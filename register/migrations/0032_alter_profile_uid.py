# Generated by Django 5.0.7 on 2024-09-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0031_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001C5F4BC5F80>', max_length=200),
        ),
    ]
