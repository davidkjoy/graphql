# Generated by Django 3.0.4 on 2020-03-20 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='university',
            new_name='universities',
        ),
    ]
