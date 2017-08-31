from django.forms import ModelForm
from core.models import SportsCenter, Court


class SportsCenterForm(ModelForm):
    class Meta:
        model = SportsCenter
        exclude = ['owner']


class CourtForm(ModelForm):
    class Meta:
        model = Court
        exclude = ['sports_center']
