# Generated by Django 5.1.1 on 2024-09-09 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='group_name',
            new_name='group',
        ),
    ]
