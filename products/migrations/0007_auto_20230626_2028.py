# Generated by Django 3.2.1 on 2023-06-26 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_products_time_posted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='category_images/')),
                ('category', models.CharField(choices=[('Cellphones and Tablets', 'Cellphones and Tablets'), ('Laptops and Computers', 'Laptops and Computers'), ('Electronic Gadgets', 'Electronic Gadgets'), ('Tech Accessories', 'Tech Accessories'), ('Appliances', 'Appliances'), ('Shoes', 'Shoes'), ('Watches and Accessories', 'Watches and Accessories'), ('Beauty and Cosmetics', 'Beauty and Cosmetics'), ('Books and Toys', 'Books and Toys'), ('Others', 'Others')], max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.ManyToManyField(default='', to='products.ProductCategory'),
        ),
    ]
