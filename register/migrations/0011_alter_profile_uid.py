# Generated by Django 5.0.7 on 2024-08-17 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0010_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001929BCD5EE0>', max_length=200),
        ),
    ]
