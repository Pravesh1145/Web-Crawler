# Generated by Django 2.1.5 on 2019-02-24 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190224_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deals',
            name='mrp',
            field=models.DecimalField(db_column='deals_mrp', decimal_places=2, default=0, max_digits=11),
        ),
        migrations.AlterField(
            model_name='deals',
            name='price',
            field=models.DecimalField(db_column='deals_price', decimal_places=2, default=0, max_digits=11),
        ),
    ]
