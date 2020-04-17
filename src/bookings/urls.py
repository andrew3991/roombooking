from django.urls import path
# from . import views
from bookings.views import BookingListView, BookingDeleteView, BookingBookView, BookingUpdateView

app_name = 'bookings'
urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:id>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
    path('<int:id>/book/', BookingBookView.as_view(), name='room-book'),
    path('<int:id>/update/', BookingUpdateView.as_view(), name='booking-update')
]
