from django.contrib import admin
from .models import RecordModel
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(RecordModel)
class RecordModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'payment', 'amount', 'category', 'date']
    list_filter = ['user', 'type', 'payment', 'category', 'date']
