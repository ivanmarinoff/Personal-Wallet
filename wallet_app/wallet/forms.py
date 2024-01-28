from django import forms

from wallet_app.wallet.models import RecordModel


class RecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__clear_fields_helper_text()

        for field_name in ['type', 'category', 'sub_category', 'payment', 'amount']:
            self.fields[field_name].help_text = 'This field is required.'

    def __clear_fields_helper_text(self):
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RecordModel
        fields = '__all__'
        exclude = ['user']
        labels = {
            'type': 'Type',
            'category': 'Category',
            'sub_category': 'Sub Category',
            'payment': 'Payment',
            'amount': 'Amount',
            'date': 'Date',
            'time': 'Time',
        }