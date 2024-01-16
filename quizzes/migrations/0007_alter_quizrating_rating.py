# Generated by Django 4.2.7 on 2024-01-16 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_alter_quizrating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizrating',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')]),
        ),
    ]
