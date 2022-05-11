from django import forms
from django.core.exceptions import ValidationError
import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        date = self.cleaned_data['renewal_date']

        #Verifica se a data de renovação adicionada está no passado
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        #Verifica se a data de renovação adicionada tem mais do que 3 semanas no futuro
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return date