from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import Building, Room, Interval, RoomFeature
from bookings.models import Booking
from django_filters import rest_framework as filters



class AddBuilding(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'

class AddRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class AddInterval(forms.ModelForm):
    class Meta:
        model = Interval
        fields = '__all__'

class AddFeature(forms.ModelForm):
    class Meta:
        model = RoomFeature
        fields = '__all__'

class RoomSearchForm(forms.ModelForm):
    #interval = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Room
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class BuildingDateForm(forms.Form):
    date = forms.DateField(widget=DateInput)