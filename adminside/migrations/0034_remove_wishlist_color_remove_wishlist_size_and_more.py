# Generated by Django 5.0.7 on 2024-10-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0033_wishlist_color_wishlist_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='color',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='size',
        ),
        migrations.AddField(
            model_name='order',
            name='return_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Return Requested', 'Return Requested'), ('Returned', 'Returned'), ('Return Rejected', 'Return Rejected')], default='Pending', max_length=20),
        ),
    ]
