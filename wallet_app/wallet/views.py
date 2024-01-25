from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

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
#
#
# class OnlyAnonymousMixin(AccessMixin):
#     login_url = "login"
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('home_page')
#         return super().dispatch(request, *args, **kwargs)
#
#
# class LandingView(OnlyAnonymousMixin, TemplateView):
#     template_name = "landing.html"
#
#
# class RegisterView(OnlyAnonymousMixin, View):
#     template_name = "register.html"
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("dashboard")
#         form = RegisterUserForm()
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request):
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get("username")
#             messages.success(request, f"Account was created for {user}")
#             return redirect("login")
#         return render(request, self.template_name, {"form": form})
#
#
# class LoginView(OnlyAnonymousMixin, View):
#     template_name = "login.html"
#     redirect_authenticated_user = True
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("dashboard")
#         return render(request, self.template_name)
#
#     def post(self, request):
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect("dashboard")
#         else:
#             messages.info(request, "Username or password is incorrect")
#             return render(request, self.template_name)
#
#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect("/")


class DashboardView(View):
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


# class LineChartDataView(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request):
#         # user = get_object_or_404(User, pk=id)
#         # Total and balance
#         total_earnings = RecordModel.objects.filter(type="Income").aggregate(
#             Sum("amount")
#         )
#         total_expenses = RecordModel.objects.filter(type="Expense").aggregate(
#             Sum("amount")
#         )
#
#         earnings_sum = total_earnings.get("amount__sum") or 0
#         expenses_sum = total_expenses.get("amount__sum") or 0
#
#         cash_balance = earnings_sum - expenses_sum
#         date_today = datetime.now()
#
#         # This month
#         month_first_day, next_month_first_day = self.get_month_range(date_today)
#         month_earnings, month_expenses = self.get_month_data(
#             month_first_day, next_month_first_day
#         )
#
#         # Last 6 months
#         n = 6
#         labels, data_earnings, data_expenses = self.get_last_n_months_data(
#             date_today, n
#         )
#
#         data = {
#             "labels": labels,
#             "data_earnings": data_earnings,
#             "data_expenses": data_expenses,
#         }
#
#         return Response(data)
#
#     def get_month_range(self, date_today):
#         month_first_day = date_today.replace(
#             day=1, hour=0, minute=0, second=0, microsecond=0
#         )
#         next_month = (date_today.replace(day=1) + timedelta(days=32)).replace(
#             day=1, hour=0, minute=0, second=0, microsecond=0
#         )
#         next_month_first_day = next_month.replace(
#             day=1, hour=0, minute=0, second=0, microsecond=0
#         )
#         return month_first_day, next_month_first_day
#
#     def get_month_data(self, month_first_day, next_month_first_day):
#         # user = get_object_or_404(User, pk=id)
#         month = RecordModel.objects.filter(
#             date__range=(month_first_day, next_month_first_day)
#         )
#         month_earnings = month.filter(type="Income").aggregate(Sum("amount"))
#         month_expenses = month.filter(type="Expense").aggregate(Sum("amount"))
#         month_earnings = month_earnings.get("amount__sum") or 0
#         month_expenses = month_expenses.get("amount__sum") or 0
#         month_cash_balance = month_earnings - month_expenses
#         return month_earnings, month_expenses
#
#     def get_last_n_months_data(self, date_today, n):
#         labels = []
#         data_earnings = []
#         data_expenses = []
#
#         for i in range(n):
#             first_day, last_day = self.get_month_range(
#                 date_today - timedelta(days=32 * (i + 1))
#             )
#             month_data = self.get_month_data(first_day, last_day)
#             month_earnings, month_expenses = month_data
#
#             labels.insert(0, first_day.strftime("%B"))
#             data_earnings.insert(0, month_earnings)
#             data_expenses.insert(0, month_expenses)
#
#         return labels, data_earnings, data_expenses

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


# class RecordView(View):
#     template_name = "records.html"
#
#     def get(self, request, pk):
#         form = RecordForm(initial={'user': request.user})
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request, pk):
#         form = RecordForm(request.POST)
#         if form.is_valid():
#             print('form is valid')
#             RecordModel.objects.create(
#                 type=request.POST.get("type"),
#                 category=request.POST.get("category"),
#                 sub_category=request.POST.get("sub_category"),
#                 payment=request.POST.get("payment"),
#                 amount=request.POST.get("amount"),
#                 date=request.POST.get("date"),
#                 time=request.POST.get("time"),
#             )
#             user = get_object_or_404(User, pk=pk)
#
#             record = form.save(commit=False)
#             print("Record saved:", record)
#             form.instance.user = request.user
#             form.save()
#             return HttpResponseRedirect("/reports")
#         else:
#             print('form is not valid', form.errors)
#         return render(request, self.template_name, {"form": form})

class RecordView(View):
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
        return render(request, self.template_name, {"form": form})

class ReportsView(View):
    template_name = "reports.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        posts = RecordModel.objects.all().filter(user=user).order_by("-date")
        context = {"posts": posts}
        return render(request, self.template_name, context)


class DeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        RecordModel.objects.filter(user=user).delete()
        return HttpResponseRedirect(f"/reports/{pk}/")
