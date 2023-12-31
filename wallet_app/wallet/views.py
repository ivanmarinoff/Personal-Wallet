from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import RecordForm, CreateUserForm
from .models import RecordModel
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

User = get_user_model()


class LandingView(TemplateView):
    template_name = "landing.html"


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = CreateUserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {user}")
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, "Username or password is incorrect")
            return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request):
        total_earnings = RecordModel.objects.filter(type="Income").aggregate(
            Sum("amount")
        )
        total_expenses = RecordModel.objects.filter(type="Expense").aggregate(
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
        month_earnings = month_data.filter(type="Income").aggregate(Sum("amount"))
        month_expenses = month_data.filter(type="Expense").aggregate(Sum("amount"))
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

    def get(self, request, format=None):
        # Total and balance
        total_earnings = RecordModel.objects.filter(type="Income").aggregate(
            Sum("amount")
        )
        total_expenses = RecordModel.objects.filter(type="Expense").aggregate(
            Sum("amount")
        )

        earnings_sum = total_earnings.get("amount__sum") or 0
        expenses_sum = total_expenses.get("amount__sum") or 0

        cash_balance = earnings_sum - expenses_sum
        date_today = datetime.now()

        # This month
        month_first_day, next_month_first_day = self.get_month_range(date_today)
        month_earnings, month_expenses = self.get_month_data(
            month_first_day, next_month_first_day
        )

        # Last 6 months
        n = 6
        labels, data_earnings, data_expenses = self.get_last_n_months_data(
            date_today, n
        )

        data = {
            "labels": labels,
            "data_earnings": data_earnings,
            "data_expenses": data_expenses,
        }

        return Response(data)

    def get_month_range(self, date_today):
        month_first_day = date_today.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        next_month = (date_today.replace(day=1) + timedelta(days=32)).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        next_month_first_day = next_month.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return month_first_day, next_month_first_day

    def get_month_data(self, month_first_day, next_month_first_day):
        month = RecordModel.objects.filter(
            date__range=(month_first_day, next_month_first_day)
        )
        month_earnings = month.filter(type="Income").aggregate(Sum("amount"))
        month_expenses = month.filter(type="Expense").aggregate(Sum("amount"))
        month_earnings = month_earnings.get("amount__sum") or 0
        month_expenses = month_expenses.get("amount__sum") or 0
        month_cash_balance = month_earnings - month_expenses
        return month_earnings, month_expenses

    def get_last_n_months_data(self, date_today, n):
        labels = []
        data_earnings = []
        data_expenses = []

        for i in range(n):
            first_day, last_day = self.get_month_range(
                date_today - timedelta(days=32 * (i + 1))
            )
            month_data = self.get_month_data(first_day, last_day)
            month_earnings, month_expenses = month_data

            labels.insert(0, first_day.strftime("%B"))
            data_earnings.insert(0, month_earnings)
            data_expenses.insert(0, month_expenses)

        return labels, data_earnings, data_expenses


class BarChartDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # Find all sum of expenses for each category
        # group by sum equivalen with annotate and values
        Query = (
            RecordModel.objects.filter(type="Expense")
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


class RecordView(View):
    template_name = "records.html"

    def get(self, request):
        form = RecordForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RecordForm(request.POST)
        if form.is_valid():
            RecordModel.objects.create(
                type=request.POST.get("type"),
                category=request.POST.get("category"),
                sub_category=request.POST.get("sub_category"),
                payment=request.POST.get("payment"),
                amount=request.POST.get("amount"),
                date=request.POST.get("date"),
                time=request.POST.get("time"),
            )
            return HttpResponseRedirect("/reports")
        return render(request, self.template_name, {"form": form})


class ReportsView(View):
    template_name = "reports.html"

    def get(self, request):
        posts = RecordModel.objects.all()
        context = {"posts": posts}
        return render(request, self.template_name, context)


class DeleteView(View):
    def get(self, request, delete_id):
        RecordModel.objects.filter(id=delete_id).delete()
        return HttpResponseRedirect("/reports")
