# Generated by Django 4.2 on 2023-04-23 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment1', '0011_alter_transaction_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='CHILDREN',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]