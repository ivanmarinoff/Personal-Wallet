# Generated by Django 5.0.1 on 2024-01-20 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0003_recordmodel_remove_expense_budget_delete_balance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recordmodel",
            name="time",
            field=models.TimeField(auto_now_add=True),
        ),
    ]
