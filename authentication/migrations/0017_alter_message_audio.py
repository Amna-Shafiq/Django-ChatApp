# Generated by Django 4.2 on 2023-06-21 13:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0016_alter_message_audio'),
    ]
    operations = [
        migrations.AlterField(
            model_name='message',
            name='audio',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
