# Generated by Django 4.2.10 on 2024-04-16 18:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_remove_imagemodel_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_address',
            field=models.TextField(default='Old Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='company_registration_number',
            field=models.CharField(default=0, max_length=9, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='registered_users',
            field=models.ManyToManyField(related_name='registered_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
