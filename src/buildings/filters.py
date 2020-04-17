from django import forms
from .models import Room, RoomFeature
import django_filters

class RoomFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    features = django_filters.ModelMultipleChoiceFilter(queryset=RoomFeature.objects.all(),
                                                      widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Room
        fields = ['room_number', 'features', 'description', 'floor', 'capacity', ]