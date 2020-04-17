from django.db import models
from users.models import User
from companies.models import Company

METHOD_CHOICES = (
    ('Booked', 'Booked'),
    ('Free', 'Free')
)

class Building(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, name='company')
    title = models.CharField(max_length=30, default='Building title', name='title')
    floor_count = models.PositiveIntegerField(verbose_name='Floors number', null=True, name='floor_count')
    address = models.TextField(max_length=200, name='address')

    def __str__(self):
        return self.title


class RoomFeature(models.Model):
    feature = models.CharField(max_length=30, name='feature')

    def __str__(self):
        return '%s' % (self.feature)


class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    # time_interval = models.ForeignKey(Interval, on_delete=models.CASCADE, null=True)
    room_number = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=200)
    floor = models.PositiveIntegerField(verbose_name="Floor number", null=True)
    capacity = models.PositiveIntegerField(verbose_name='Capacity', null=True)
    beamer = models.BooleanField(default=False)
    board = models.BooleanField(default=False)
    #    tool = models.ForeignKey(RoomFeature, on_delete=models.CASCADE, null=True)
    features = models.ManyToManyField(RoomFeature, blank=True)

    def __str__(self):
        return '%s - %s' % (self.building, self.room_number)


class Interval(models.Model):
    # building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=30, choices=METHOD_CHOICES, default='Free')

    def __str__(self):
        return '%s - %s' % (self.start_time, self.end_time)

    # def save(self, *args, **kwargs):
    #     if self.floor is None:
    #         self.floor.default = self.building.floor_count
    #     super(Room, self).save(*args, **kwargs)




