# Generated by Django 2.1.5 on 2020-02-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesys', '0022_pack'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtu',
            name='Rise',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='rtu',
            name='RiseDataType',
            field=models.CharField(default='', max_length=255),
        ),
    ]