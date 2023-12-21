# urls.py
from django.urls import path
from .views import BudgetView

urlpatterns = [
    path('', BudgetView.as_view(), name='budget-view'),
    # Add other URLs as needed
]
