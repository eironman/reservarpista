from django import forms
from core.models import Location, Sport


TIME_CHOICES = (
    ('00:00', 'Cualquiera'),
    ('08:00', '08:00'),
    ('08:30', '08:30'),
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('12:30', '12:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
    ('17:00', '17:00'),
    ('17:30', '17:30'),
    ('18:00', '18:00'),
    ('18:30', '18:30'),
    ('19:00', '19:00'),
    ('19:30', '19:30'),
    ('20:00', '20:00'),
    ('20:30', '20:30'),
    ('21:00', '21:00'),
    ('21:30', '21:30'),
    ('22:00', '22:00'),
    ('22:30', '22:30'),
    ('23:00', '23:00'),
)

DURATION_CHOICES = (
    (60, '60 minutos'),
    (90, '90 minutos'),
    (120, '120 minutos'),
)


def get_sports_choices():
    """Options for sport select"""
    sports = Sport.objects.all()
    choices = []
    for sport in sports:
        sport_tuple = (sport.slug, sport.name)
        choices.append(sport_tuple)
    return choices


def get_locations_choices():
    """Options for location select"""
    locations = Location.objects.all()
    choices = []
    for location in locations:
        location_tuple = (location.slug, location.name)
        choices.append(location_tuple)
    return choices


class SearchSportForm(forms.Form):
    """Search form"""
    location = forms.ChoiceField(label='Ubicación', choices=get_locations_choices())
    sport = forms.ChoiceField(label='Deporte', choices=get_sports_choices())
    time = forms.ChoiceField(label='Hora', choices=TIME_CHOICES)
    duration = forms.ChoiceField(label='Tiempo', choices=DURATION_CHOICES)
    date = forms.DateField(label='Día', input_formats=['%Y/%m/%d'], required=False)

    date.widget.attrs['class'] = 'datepicker'
    date.widget.attrs['placeholder'] = 'Cualquiera'

    def __init__(self, *args, **kwargs):
        if args and args[0] is not None:
            # Default value for pickadate.js
            if 'date' in args[0] is not None and args[0]['date'] is not '':
                self.declared_fields['date'].widget.attrs['data-value'] = args[0]['date']
            else:
                self.declared_fields['date'].widget.attrs['data-value'] = ''
            # Selected sport
            if 'sport' in args[0] is not None and args[0]['sport'] is not '':
                self.declared_fields['sport'].initial = args[0]['sport']
            # Selected location
            if 'location' in args[0] is not None and args[0]['location'] is not '':
                self.declared_fields['location'].initial = args[0]['location']

        super(SearchSportForm, self).__init__(*args, **kwargs)

























