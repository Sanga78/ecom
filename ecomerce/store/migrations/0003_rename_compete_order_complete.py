# Generated by Django 5.0.2 on 2024-02-26 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='compete',
            new_name='complete',
        ),
    ]