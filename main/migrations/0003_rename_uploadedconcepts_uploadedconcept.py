# Generated by Django 4.1.2 on 2022-10-20 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_uploadedconcepts_delete_definitiontohtml'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadedConcepts',
            new_name='UploadedConcept',
        ),
    ]