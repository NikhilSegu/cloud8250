# Generated by Django 4.2 on 2023-04-22 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment1', '0010_alter_household_hshd_num_alter_product_product_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='PURCHASE',
            field=models.CharField(max_length=100),
        ),
    ]
