from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    LandingView,
    RegisterView,
    LoginView,
    LogoutView,
    DashboardView,
    LineChartDataView,
    BarChartDataView,
    RecordView,
    ReportsView,
    DeleteView,
)

urlpatterns = [
                  path('register/', RegisterView.as_view(), name='register'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('', LandingView.as_view(), name='landing'),
                  path('records/', RecordView.as_view(), name='records'),
                  path('reports/', ReportsView.as_view(), name='reports'),
                  path('dashboard/', DashboardView.as_view(), name='dashboard'),
                  path('reports/delete/<str:delete_id>/', DeleteView.as_view(), name='delete'),
                  path('api/linechart/data/', LineChartDataView.as_view(), name='line-chart-data'),
                  path('api/barchart/data/', BarChartDataView.as_view(), name='bar-chart-data'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
