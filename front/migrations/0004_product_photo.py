# Generated by Django 4.2 on 2023-04-30 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_rename_user_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.CharField(default='default.jpg', max_length=100),
        ),
    ]
