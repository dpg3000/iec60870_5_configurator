# Generated by Django 2.1.5 on 2020-02-04 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_parts', '0027_auto_20200130_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objsinfo',
            name='ObjType',
            field=models.CharField(choices=[('MONITOR', 'MONITOR'), ('CONTROL', 'CONTROL')], max_length=255),
        ),
    ]