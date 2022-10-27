# Generated by Django 4.1.2 on 2022-10-27 04:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("stockKR", "0002_rename_stocktype_krstockelementmodel_stock_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stockkr",
            name="first_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="stockkr",
            name="last_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]