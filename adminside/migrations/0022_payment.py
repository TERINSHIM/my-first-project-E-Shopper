# Generated by Django 5.0.7 on 2024-09-02 15:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0021_product_color_product_size'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
