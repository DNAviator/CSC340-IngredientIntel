# Generated by Django 5.0.2 on 2024-04-10 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_company_products_remove_ingredient_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='item_id',
            field=models.TextField(blank=True),
        ),
    ]
