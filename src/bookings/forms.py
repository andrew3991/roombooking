from django import forms
from .models import Booking, Interval


class BookingConfirmForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Booking
        fields = 'message'


class BookingUpdateForm(forms.ModelForm):
    #interval = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Booking
        fields = ('user', 'interval', 'status')

    def __init__(self, *args, **kwargs):
        interval = kwargs.pop('interval')
        super().__init__(*args, **kwargs)
        self.fields['interval'].queryset = interval



    # def save(self):
    #     habit = super(BookingUpdateForm, self).save()
    #     habit.user = self.cleaned_data['user']
    #     habit.interval = self.cleaned_data['interval']
    #     habit.status = self.cleaned_data['status']
    #     habit.message = self.cleaned_data['message']
    #     habit.save()
