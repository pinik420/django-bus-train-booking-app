from datetime import timedelta, datetime
from .models import *
from .models import Week
from tqdm import tqdm
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from .models import *
import secrets
from xhtml2pdf import pisa

def get_number_of_lines(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def createWeekDays():
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i,day in enumerate(days):
        Week.objects.create(number=i, name=day)

FEE = 10.0

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def createBusticket(user,passengers,passengerscount,bus1,bus_1date,bus_1class,coupon,countrycode,email,mobile):
    ticket = BusTicket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    for passenger in passengers:
        ticket.passengers.add(passenger)
    ticket.bus = bus1
    ticket.bus_ddate = datetime(int(bus_1date.split('-')[2]),int(bus_1date.split('-')[1]),int(bus_1date.split('-')[0]))
    ###################
    bus1ddate = datetime(int(bus_1date.split('-')[2]),int(bus_1date.split('-')[1]),int(bus_1date.split('-')[0]),bus1.depart_time.hour,bus1.depart_time.minute)
    bus1adate = (bus1ddate + bus1.duration)
    ###################
    ticket.bus_adate = datetime(bus1adate.year,bus1adate.month,bus1adate.day)
    ffre = 0.0
    if bus_1class.lower() == 'first':
        ticket.bus_fare = bus1.first_fare*int(passengerscount)
        ffre = bus1.first_fare*int(passengerscount)
    elif bus_1class.lower() == 'business':
        ticket.bus_fare = bus1.business_fare*int(passengerscount)
        ffre = bus1.business_fare*int(passengerscount)
    else:
        ticket.bus_fare = bus1.economy_fare*int(passengerscount)
        ffre = bus1.economy_fare*int(passengerscount)
    ticket.other_charges = FEE
    if coupon:
        ticket.coupon_used = coupon                     ##########Coupon
    ticket.total_fare = ffre+FEE+0.0                    ##########Total(Including coupon)
    ticket.seat_class = bus_1class.lower()
    ticket.status = 'PENDING'
    ticket.mobile = ('+'+countrycode+' '+mobile)
    ticket.email = email
    ticket.save()
    return ticket

def createTrainticket(user,passengers,passengerscount,train1,train_1date,train_1class,coupon,countrycode,email,mobile):
    ticket = TrainTicket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    for passenger in passengers:
        ticket.passengers.add(passenger)
    ticket.train = train1
    ticket.train_ddate = datetime(int(train_1date.split('-')[2]),int(train_1date.split('-')[1]),int(train_1date.split('-')[0]))
    ###################
    train1ddate = datetime(int(train_1date.split('-')[2]),int(train_1date.split('-')[1]),int(train_1date.split('-')[0]),train1.depart_time.hour,train1.depart_time.minute)
    train1adate = (train1ddate + train1.duration)
    ###################
    ticket.train_adate = datetime(train1adate.year,train1adate.month,train1adate.day)
    ffre = 0.0
    if train_1class.lower() == 'first':
        ticket.train_fare = train1.first_fare*int(passengerscount)
        ffre = train1.first_fare*int(passengerscount)
    elif train_1class.lower() == 'business':
        ticket.train_fare = train1.business_fare*int(passengerscount)
        ffre = train1.business_fare*int(passengerscount)
    else:
        ticket.train_fare = train1.economy_fare*int(passengerscount)
        ffre = train1.economy_fare*int(passengerscount)
    ticket.other_charges = FEE
    if coupon:
        ticket.coupon_used = coupon                     ##########Coupon
    ticket.total_fare = ffre+FEE+0.0                    ##########Total(Including coupon)
    ticket.seat_class = train_1class.lower()
    ticket.status = 'PENDING'
    ticket.mobile = ('+'+countrycode+' '+mobile)
    ticket.email = email
    ticket.save()
    return ticket