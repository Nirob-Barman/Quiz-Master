# Generated by Django 4.2.7 on 2024-01-15 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='text',
            new_name='quizAnswer',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='quiz',
            new_name='quizQuestion',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
    ]
