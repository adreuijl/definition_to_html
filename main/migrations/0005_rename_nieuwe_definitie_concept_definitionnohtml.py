# Generated by Django 4.1.2 on 2022-10-27 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_match'),
    ]

    operations = [
        migrations.RenameField(
            model_name='concept',
            old_name='nieuwe_definitie',
            new_name='definitionNoHtml',
        ),
    ]
