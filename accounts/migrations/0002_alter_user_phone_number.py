# Generated by Django 5.0.6 on 2024-06-03 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(db_index=True, max_length=11, unique=True),
        ),
    ]
