# views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm


class BudgetView(View):
    template_name = 'budget.html'

    def get(self, request):
        budget = Budget.objects.first()
        expenses = Expense.objects.all()
        budget_form = BudgetForm(instance=budget)
        expense_form = ExpenseForm()
        return render(request, self.template_name, {
            'budget': budget,
            'expenses': expenses,
            'budget_form': budget_form,
            'expense_form': expense_form,
        })

    def post(self, request):
        budget = Budget.objects.first()
        expenses = Expense.objects.all()
        budget_form = BudgetForm(request.POST, instance=budget)
        expense_form = ExpenseForm(request.POST)

        if budget_form.is_valid():
            budget_form.save()

        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.budget = budget
            expense.save()

        return redirect('budget-view')  # Change to your URL name
