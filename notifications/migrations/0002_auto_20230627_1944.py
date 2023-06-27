# Generated by Django 3.2.1 on 2023-06-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.ManyToManyField(default='', to='notifications.NotificationCategory'),
        ),
        migrations.AlterField(
            model_name='notificationcategory',
            name='image',
            field=models.ImageField(upload_to='notifications/'),
        ),
    ]
