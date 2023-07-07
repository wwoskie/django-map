# Generated by Django 4.2.3 on 2023-07-07 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_datamapinstance_federal_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='datagraphinstance',
            name='federal_district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='maps.federaldistrict'),
        ),
    ]
