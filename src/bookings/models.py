from django.db import models
from buildings.models import Interval, Room
from users.models import User


METHOD_CHOICES = (
    ('Approved', 'Approved'),
    ('Canceled', 'Canceled'),
    ('Pending', 'Pending')
)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, choices=METHOD_CHOICES, default='Pending')
    created = models.DateTimeField(verbose_name='Create', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    reservation_date = models.CharField(max_length=10, null=True)
    message = models.TextField(max_length=200, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
