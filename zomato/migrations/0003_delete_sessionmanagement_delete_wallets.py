# Generated by Django 4.1.5 on 2023-01-26 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("zomato", "0002_sessionmanagement"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SessionManagement",
        ),
        migrations.DeleteModel(
            name="Wallets",
        ),
    ]
