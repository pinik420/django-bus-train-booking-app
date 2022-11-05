from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

GENDER = (
    ('male','MALE'),   
    ('female','FEMALE')
)

SEAT_CLASS = (
    ('economy', 'Economy'),
    ('business', 'Business'),
    ('first', 'First')
)

TICKET_STATUS =(
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled')
)

class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.number})"



class User(AbstractUser):
    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"
        

class Railway(models.Model):
    city = models.CharField(max_length=64)
    railway = models.CharField(max_length=64)
    code = models.CharField(max_length=3)
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.code})"

class Busstop(models.Model):
    city = models.CharField(max_length=64)
    busstop = models.CharField(max_length=64)
    code = models.CharField(max_length=3)
    country = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.code})"

class Train(models.Model):
    origin = models.ForeignKey(Railway, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Railway, on_delete=models.CASCADE, related_name="arrivals")
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.ManyToManyField(Week, related_name="trains_of_the_day")
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    train = models.CharField(max_length=24)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

class Bus(models.Model):
    origin = models.ForeignKey(Busstop, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Busstop, on_delete=models.CASCADE, related_name="arrivals")
    depart_time = models.TimeField(auto_now=False, auto_now_add=False)
    depart_day = models.ManyToManyField(Week, related_name="buses_of_the_day")
    duration = models.DurationField(null=True)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    bus = models.CharField(max_length=24)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"


class Passenger(models.Model):
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)
    #passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flights")
    #flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="passengers")

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}, {self.gender}"


class TrainTicket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="train_bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True)
    passengers = models.ManyToManyField(Passenger, related_name="train_tickets")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    train_ddate = models.DateField(blank=True, null=True)
    train_adate = models.DateField(blank=True, null=True)
    train_fare = models.FloatField(blank=True,null=True)
    other_charges = models.FloatField(blank=True,null=True)
    coupon_used = models.CharField(max_length=15,blank=True)
    coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return self.ref_no

class BusTicket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bus_bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True)
    passengers = models.ManyToManyField(Passenger, related_name="bus_tickets")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    bus_ddate = models.DateField(blank=True, null=True)
    bus_adate = models.DateField(blank=True, null=True)
    bus_fare = models.FloatField(blank=True,null=True)
    other_charges = models.FloatField(blank=True,null=True)
    coupon_used = models.CharField(max_length=15,blank=True)
    coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)

    def __str__(self):
        return self.ref_no