# Generated by Django 4.2 on 2023-06-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_message_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='audio',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
