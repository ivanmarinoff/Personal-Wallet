from django import forms
from .models import Budget, Expense


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount']


class BalanceForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['balance']
