# Generated by Django 3.2.1 on 2023-06-23 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20230623_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='time_posted',
            field=models.TimeField(),
        ),
    ]