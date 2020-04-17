from .models import Building, Room, Interval, RoomFeature
from bookings.models import Booking
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .choices import *
from django.http import HttpResponseRedirect
from .forms import AddBuilding, AddRoom, AddInterval, AddFeature, RoomSearchForm, BuildingDateForm
from .filters import RoomFilter
from django.contrib.auth.decorators import user_passes_test



class BuildingSearchDateView(ListView):
    model = Building
    # context_object_name = 'building_list'
    template_name = "buildings/search_building.html"
    form_class = BuildingDateForm

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the rooms
        form = self.form_class()
        context['form'] = form

        return context

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            # # create booking object
            date = form.cleaned_data['date']

            #return render(self.request, reverse('buildings:building-list'), {'date': date})
            return HttpResponseRedirect(reverse('buildings:building-list', args=(date,)))
        return render(self.request, self.template_name, {'form': form})

class BuildingListView(ListView):
    model = Building
    # context_object_name = 'building_list'
    template_name = "buildings/buildings_list.html"
    form_class = RoomSearchForm

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the rooms
        form = self.form_class()
        #context['rooms'] = Room.objects.all()
        #context['rooms_filter'] = RoomFilter(**kwargs, queryset=context['rooms'])
        rooms = Room.objects.all()
        rooms_filter = RoomFilter(self.request.GET, queryset=rooms)
        self.request.session["date"] = self.kwargs['date']
        date_ = self.kwargs['date']
        context['intervals'] = Interval.objects.all()
        context['user'] = self.request.user
        context['buildings'] = Building.objects.all()
        context['form'] = form
        context['filter'] = rooms_filter
        for n in context['buildings']:
            n.floor_count = range(1, n.floor_count + 1)

        for i in context['intervals']:
            # f = {'interval_id': i.id}
            booking = Booking.objects.filter(interval_id=i.id)
            for b in booking:
                if b:
                    if b.reservation_date == date_:
                        i.status = 'Booked'
                        i.save()
                    else:
                        i.status = 'Free'
                        i.save()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        #interval_id = kwargs['id']
        if form.is_valid():
            # # create booking object
            datasetfromform = form.cleaned_data['features']
            for i in datasetfromform:
                print(i)
            # if 'building' in request.GET:
            #     building = request.GET['building']
            #     if building:
            #         queryset_list = building_list.filter(title__iexact=building)
            # message_ = form.cleaned_data['message']
            # user_ = User.objects.get(id=request.user.id)
            # interval_ = Interval.objects.get(id=interval_id)
            # room_ = Room.objects.get(id=interval_.room_id)
            # obj = Booking(user_id=user_.id, interval_id=interval_.id, message=message_, room_id=room_.id)
            # obj.save()
            #
            # # update status room interval object
            # i = Interval.objects.get(id=interval_id)
            # i.status = 'Booked'
            # i.save()

            return HttpResponseRedirect('/buildings/')
        return render(request, self.template_name, {'form': form})





def search(request):
    queryset_list = Room.objects.order_by('-room_number')
    building_list = Building.objects.all()
    building_list_query = Building.objects.all()
    time_list_query = Interval.objects.all()
    feature_list_query = RoomFeature.objects.all()
    for n in building_list:
        n.floor_count = range(1, n.floor_count + 1)

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # Room Number
    if 'room_number' in request.GET:
        room_number = request.GET['room_number']
        if room_number:
            queryset_list = queryset_list.filter(room_number__iexact=room_number)

    # Buildings
    if 'building' in request.GET:
        building = request.GET['building']
        if building:
            queryset_list = building_list.filter(title__iexact=building)

    # Features
    if 'feature' in request.GET:
        feature = request.GET.getlist('feature')
        if feature:
            queryset_list = feature_list_query.filter(feature__in=feature)

    context = {
        'feature_list_query': feature_list_query,
        'board_choices': board_choices,
        'room_list': queryset_list,
        'building_list': building_list,
        'values': request.GET,
        'building_list_query': building_list_query,
        'time_list_query': time_list_query
    }

    return render(request, 'buildings/search.html', context)


@user_passes_test(lambda u: u.is_admin, login_url="/users/profile")
def addbuilding(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddBuilding(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/buildings/thanksb/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddBuilding()

    return render(request, 'buildings/addbuilding.html', {'form': form})

@user_passes_test(lambda u: u.is_admin, login_url="/users/profile")
def addroom(request):
    if request.method == 'POST':
        form = AddRoom(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/buildings/thanksr/')
    else:
        form = AddRoom()
    return render(request, 'buildings/addroom.html', {'form': form})

@user_passes_test(lambda u: u.is_admin and u.is_advanceduser, login_url="/users/profile")
def addinterval(request):
    if request.method == 'POST':
        form = AddInterval(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/buildings/thanksi/')
    else:
        form = AddInterval()
    return render(request, 'buildings/addinterval.html', {'form': form})

@user_passes_test(lambda u: u.is_admin and u.is_advanceduser, login_url="/users/profile")
def addfeature(request):
    if request.method == 'POST':
        form = AddFeature(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/buildings/thanksf/')
    else:
        form = AddFeature()
    return render(request, 'buildings/addfeature.html', {'form': form})

def thanksb(request):
    return render(request, 'buildings/thanksb.html')

def thanksr(request):
    return render(request, 'buildings/thanksr.html')

def thanksi(request):
    return render(request, 'buildings/thanksi.html')

def thanksf(request):
    return render(request, 'buildings/thanksf.html')


@user_passes_test(lambda u: u.is_advanceduser and u.is_admin, login_url="/users/profile")
def editroom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == "POST":
        form = AddRoom(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect('buildings:building-search-date')
    else:
        form = AddRoom(instance=room)
    return render(request, 'buildings/editroom.html', {'form': form})
