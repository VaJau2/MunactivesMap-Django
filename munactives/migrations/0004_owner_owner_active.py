# Generated by Django 3.0.3 on 2020-03-07 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('munactives', '0003_auto_20200209_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='owner',
            fields=[
                ('owner_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('address', models.TextField()),
                ('fio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='owner_active',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_id', models.PositiveIntegerField()),
                ('active_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='munactives.owner')),
            ],
        ),
    ]
