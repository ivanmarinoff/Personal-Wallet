from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_filter = ['username', 'email']
    search_fields = ['username', 'email']

    permissions = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name="Add permissions",
            is_stacked=False
        )
    )