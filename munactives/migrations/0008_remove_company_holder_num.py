# Generated by Django 3.0.3 on 2020-03-11 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('munactives', '0007_auto_20200311_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='holder_num',
        ),
    ]