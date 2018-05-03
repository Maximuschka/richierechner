from django import forms
from django.contrib.auth.models import User
from .models import Ausgabe

from django.contrib.admin.widgets import AdminDateWidget
import datetime

class AusgabeForm(forms.ModelForm):
    datum = forms.DateField(label='Datum',initial=datetime.date.today)

    class Meta:
        model = Ausgabe
        fields = ["mitbewohni","datum","wert","an","notiz"]
        labels = {
        "mitbewohni": "Von"
    }

class AusgleichszahlungForm(forms.ModelForm):
    datum = forms.DateField(label='Datum', initial=datetime.date.today)
    an = forms.ModelChoiceField(queryset=User.objects.all().exclude(is_superuser=True))

    class Meta:
        model = Ausgabe
        fields = ["mitbewohni","an","datum","wert"]
        labels = {
        "mitbewohni": "Von"
        }

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class OverviewForm(forms.Form):
    start_datum = forms.DateField(label='Startdatum')
    end_datum = forms.DateField(label='Enddatum')