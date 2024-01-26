from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    DashboardView,
    LineChartDataView,
    BarChartDataView,
    RecordView,
    ReportsView,
    DeleteView,
)
from ..users.views import RegisterUserView, LoginUserView, LogoutUserView, LandingView

urlpatterns = [
                  path('register/', RegisterUserView.as_view(), name='register'),
                  path('login/', LoginUserView.as_view(), name='login'),
                  path('logout/', LogoutUserView.as_view(), name='logout'),
                  path('', LandingView.as_view(), name='landing'),
                  path('records/<int:pk>/', RecordView.as_view(), name='records'),
                  path('reports/<int:pk>/', ReportsView.as_view(), name='reports'),
                  path('dashboard/<int:pk>/', DashboardView.as_view(), name='dashboard'),
                  path('reports/delete/<int:pk>/<int:id>/', DeleteView.as_view(), name='delete'),
                  path('api/linechart/data/<int:pk>/', LineChartDataView.as_view(), name='line-chart-data'),
                  path('api/barchart/data/<int:id>/', BarChartDataView.as_view(), name='bar-chart-data'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)