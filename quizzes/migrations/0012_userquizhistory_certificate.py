# Generated by Django 5.0.1 on 2024-01-23 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0011_quiz_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquizhistory',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
    ]
