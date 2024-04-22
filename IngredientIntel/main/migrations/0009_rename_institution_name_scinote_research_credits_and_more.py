# Generated by Django 4.2.10 on 2024-04-22 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_company_company_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scinote',
            old_name='institution_name',
            new_name='research_credits',
        ),
        migrations.RemoveField(
            model_name='scinote',
            name='researcher_names',
        ),
        migrations.AddField(
            model_name='scinote',
            name='researcher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
