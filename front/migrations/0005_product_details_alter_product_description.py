# Generated by Django 4.2 on 2023-04-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_product_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='details',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]