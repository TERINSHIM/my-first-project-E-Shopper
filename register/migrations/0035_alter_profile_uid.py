# Generated by Django 5.0.7 on 2024-09-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0034_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000014A44245F80>', max_length=200),
        ),
    ]
