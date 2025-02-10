# Generated by Django 3.1.12 on 2025-02-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='api_user_email_a7eefd_idx'),
        ),
    ]
