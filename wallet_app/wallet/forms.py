from django import forms

from wallet_app.wallet.models import RecordModel


class RecordForm(forms.ModelForm):
    class Meta:
        model = RecordModel
        fields = '__all__'
        exclude = ['user']