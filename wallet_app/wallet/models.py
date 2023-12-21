# models.py
from django.db import models

class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
