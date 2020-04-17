from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from bookings.models import Booking
from .models import Booking, User, Interval, Room
from django.views.generic import ListView, DeleteView, UpdateView
from .forms import BookingConfirmForm, BookingUpdateForm
from django.contrib.auth.mixins import PermissionRequiredMixin
# class BookingView(View):
#     model = Booking
#     template_name = 'bookings/index.html'
#     name = "Booking"
#     context = {'name': name}
#     Booking.objects.all()
#
#     def get(self, request):
#         return render(request, self.template_name, self.context)


class BookingListView(ListView):
    template_name = 'bookings/booking_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return Booking.objects.all()

            else:
                return Booking.objects.filter(user=self.request.user)
        else:
            return render(self.request, 'bookings/error_login.html')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class BookingDeleteView(DeleteView):
    template_name = 'bookings/booking_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Booking, id=id_)

    def get_success_url(self):
        return reverse('bookings:booking-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        interval = Interval.objects.get(id=self.object.interval_id)
        interval.status = 'Free'
        interval.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class BookingBookView(View):
    template_name = 'bookings/booking_confirm.html'
    form_class = BookingConfirmForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        date_ = self.request.session['date']
        return render(request, self.template_name, {'form': form, 'date': date_})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        interval_id = kwargs['id']
        if form.is_valid():
            # create booking object
            date_ = self.request.session['date']
            #message_ = form.cleaned_data['message']
            user_ = User.objects.get(id=request.user.id)
            interval_ = Interval.objects.get(id=interval_id)
            room_ = Room.objects.get(id=interval_.room_id)
            obj = Booking(user_id=user_.id, interval_id=interval_.id, room_id=room_.id, reservation_date=date_)
            obj.save()

            # update status room interval object
            i = Interval.objects.get(id=interval_id)
            i.status = 'Booked'
            i.save()

            return HttpResponseRedirect('/buildings/'+date_)
        return render(request, self.template_name, {'form': form})


class BookingUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'u.is_admin'
    login_url = 'users/profile'
    model = Booking
    template_name = 'bookings/booking_update.html'
    form_class = BookingUpdateForm
    context_object_name = 'booking'
    #success_url = reverse('bookings:booking-list')

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Booking, id=id_)


    def get_success_url(self):
        return reverse('bookings:booking-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #kwargs['interval'] = [i for i in Interval.objects.filter(room_id=self.object.room_id)]
        kwargs['interval'] = Interval.objects.filter(room_id=self.object.room_id)
        return kwargs