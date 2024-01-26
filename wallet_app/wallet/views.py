from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from wallet_app.users.mixins import CustomLoginRequiredMixin, ErrorRedirectMixin
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import RecordForm
from .models import RecordModel
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from ..users.forms import RegisterUserForm

User = get_user_model()


class DashboardView(CustomLoginRequiredMixin, ErrorRedirectMixin, View):
    template_name = "dashboard.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        total_earnings = RecordModel.objects.filter(type="Income", user=user).aggregate(
            Sum("amount")
        )
        total_expenses = RecordModel.objects.filter(type="Expense", user=user).aggregate(
            Sum("amount")
        )
        earnings_sum = total_earnings.get("amount__sum") or 0
        expenses_sum = total_expenses.get("amount__sum") or 0
        cash_balance = earnings_sum - expenses_sum

        date_today = datetime.now()
        month_earnings, month_expenses = self.get_month_data(
            (
                date_today.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
                (date_today.replace(day=1) + timedelta(days=32)).replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                ),
            )
        )

        month_cash_balance = month_earnings - month_expenses

        # Last 6 months
        n = 6
        month_data = self.get_last_n_months_data(date_today, n)
        totals_earnings = self.get_last_n_months_totals(month_data)
        totals_expenses = self.get_last_n_months_totals(month_data)
        labels = self.get_last_n_months_labels(date_today, n)

        context = {
            "total_earnings": earnings_sum,
            "total_expenses": expenses_sum,
            "cash_balance": cash_balance,
            "month_earnings": month_earnings,
            "month_expenses": month_expenses,
            "month_cash_balance": month_cash_balance,
            "data_earnings": totals_earnings,
            "data_expenses": totals_expenses,
            "labels": labels,
        }
        return render(request, self.template_name, context)

    def get_month_data(self, date_range):
        month_data = RecordModel.objects.filter(date__range=date_range)
        month_earnings = month_data.filter(type="Income", user=self.request.user).aggregate(Sum("amount"))
        month_expenses = month_data.filter(type="Expense", user=self.request.user).aggregate(Sum("amount"))
        return (
            month_earnings.get("amount__sum") or 0,
            month_expenses.get("amount__sum") or 0,
        )

    def get_last_n_months_data(self, date_today, n):
        month_data = []
        for i in range(n):
            first_day = date_today - timedelta(days=32)
            first_day = first_day.replace(day=1)
            last_day = date_today.replace(day=1)
            month_data.append(
                RecordModel.objects.filter(date__range=(first_day, last_day))
            )
            date_today = first_day
        return month_data

    def get_last_n_months_totals(self, month_data):
        return [
            month.aggregate(Sum("amount"))["amount__sum"] or 0 for month in month_data
        ]

    def get_last_n_months_labels(self, date_today, n):
        return [date_today.strftime("%B") for _ in range(n)]


class LineChartDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        # Fetch the user object
        user = get_object_or_404(User, pk=pk)

        # Total and balance
        total_earnings = RecordModel.objects.filter(user_id=pk, type="Income").aggregate(
            Sum("amount")
        )
        total_expenses = RecordModel.objects.filter(user_id=pk, type="Expense").aggregate(
            Sum("amount")
        )

        earnings_sum = total_earnings.get("amount__sum") or 0
        expenses_sum = total_expenses.get("amount__sum") or 0

        cash_balance = earnings_sum - expenses_sum
        date_today = datetime.now()

        # This month
        month_first_day, next_month_first_day = self.get_month_range(date_today)
        month_earnings, month_expenses = self.get_month_data(
            month_first_day, next_month_first_day, user
        )

        # Last 6 months
        n = 6
        labels, data_earnings, data_expenses = self.get_last_n_months_data(
            date_today, n, user
        )

        data = {
            "labels": labels,
            "data_earnings": data_earnings,
            "data_expenses": data_expenses,
        }

        return Response(data)

    def get_month_range(self, date):
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month_start = (month_start.replace(day=1) + timedelta(days=32)).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return month_start, next_month_start

    def get_month_data(self, start_date, end_date, user):
        month_earnings = RecordModel.objects.filter(
            user=user, type="Income", date__range=[start_date, end_date]
        ).aggregate(Sum("amount")).get("amount__sum") or 0

        month_expenses = RecordModel.objects.filter(
            user=user, type="Expense", date__range=[start_date, end_date]
        ).aggregate(Sum("amount")).get("amount__sum") or 0

        return month_earnings, month_expenses

    def get_last_n_months_data(self, date, n, user):
        labels = []
        data_earnings = []
        data_expenses = []

        for i in range(n):
            month_start = (date.replace(day=1) - timedelta(days=i * 30)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            month_end = (
                    (month_start.replace(day=1) + timedelta(days=32)).replace(
                        day=1, hour=0, minute=0, second=0, microsecond=0
                    )
                    - timedelta(days=1)
            )

            month_label = month_start.strftime("%B %Y")
            labels.append(month_label)

            month_earnings = RecordModel.objects.filter(
                user=user, type="Income", date__range=[month_start, month_end]
            ).aggregate(Sum("amount")).get("amount__sum") or 0

            month_expenses = RecordModel.objects.filter(
                user=user, type="Expense", date__range=[month_start, month_end]
            ).aggregate(Sum("amount")).get("amount__sum") or 0

            data_earnings.append(month_earnings)
            data_expenses.append(month_expenses)

        return labels, data_earnings, data_expenses


class BarChartDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):

        user = get_object_or_404(User, pk=id)
        # Find all sum of expenses for each category
        # group by sum equivalen with annotate and values
        Query = (
            RecordModel.objects.filter(user=user, type="Expense")
            .values("category")
            .annotate(exp=Sum("amount"))
            .order_by("-exp")
        )
        n = []
        labels = []
        for i in Query:
            for k, v in i.items():
                if isinstance(v, float):
                    n.append(v)
                else:
                    labels.append(v)
        data = {
            "labels": labels,
            "default": n,
        }
        return Response(data)


class RecordView(CustomLoginRequiredMixin, ErrorRedirectMixin, View):
    template_name = "records.html"

    def get(self, request, pk):
        form = RecordForm(initial={'user': request.user})
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        form = RecordForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(f"/reports/{pk}/")
        else:
            print('form is not valid', form.errors)
            form.errors.clear()
        return render(request, self.template_name, {"form": form})


class ReportsView(CustomLoginRequiredMixin, ErrorRedirectMixin, View):
    template_name = "reports.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        posts = RecordModel.objects.all().filter(user=user).order_by("-date")
        context = {"posts": posts}
        return render(request, self.template_name, context)


class DeleteView(CustomLoginRequiredMixin, ErrorRedirectMixin, View):
    def get(self, request, pk, id):
        user = get_object_or_404(User, pk=pk)
        post = get_object_or_404(RecordModel, user=user, id=id)
        post.delete()
        # Check if there are any more records left for the user
        if RecordModel.objects.filter(user=user).exists():
            return HttpResponseRedirect(f"/reports/{pk}/")
        else:
            return HttpResponseRedirect(reverse_lazy('dashboard', kwargs={'pk': pk}))