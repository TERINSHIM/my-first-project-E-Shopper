# Generated by Django 5.0.7 on 2024-09-02 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0027_alter_profile_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000022E9F265F80>', max_length=200),
        ),
    ]
