# Generated by Django 3.0.3 on 2020-03-07 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('munactives', '0004_owner_owner_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='munactives.owner'),
        ),
        migrations.AddField(
            model_name='foundation',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='munactives.owner'),
        ),
        migrations.AddField(
            model_name='housing_stock',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='munactives.owner'),
        ),
        migrations.AddField(
            model_name='munitipal_land',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='munactives.owner'),
        ),
        migrations.DeleteModel(
            name='owner_active',
        ),
    ]
