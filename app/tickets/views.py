from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from datetime import datetime
import math
from .models import *
from .utils import render_to_pdf, createWeekDays, createBusticket, createTrainticket

from itertools import chain

#Fee and Surcharge variable

FEE = 10.0

try:
    if len(Week.objects.all()) == 0:
        createWeekDays()
except:
    pass

# Create your views here.

def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        if(trip_type == '1'):
            return render(request, 'travel/index.html', {
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type
        })
        elif(trip_type == '2'):
            return_date = request.POST.get('ReturnDate')
            return render(request, 'travel/index.html', {
            'min_date': min_date,
            'max_date': max_date,
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type,
            'return_date': return_date
        })
    else:
        return render(request, 'travel/index.html', {
            'min_date': min_date,
            'max_date': max_date
        })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            
        else:
            return render(request, "travel/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "travel/login.html")

def register_view(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travel/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(request, "travel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travel/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def query_railway(request, q):
    #places = Airport.objects.all()
    filters = []
    places = Railway.objects.all()
    q = q.lower()
    for place in places:
        if (q in place.city.lower()) or (q in place.railway.lower()) or (q in place.code.lower()) or (q in place.country.lower()):
            filters.append(place)
    return JsonResponse([{'code':place.code, 'place':place.railway, 'city':place.city, 'country': place.country} for place in filters], safe=False)

def query_busstop(request, q):
    #places = Airport.objects.all()
    filters = []
    places = Busstop.objects.all()
    q = q.lower()
    for place in places:
        if (q in place.city.lower()) or (q in place.busstop.lower()) or (q in place.code.lower()) or (q in place.country.lower()):
            filters.append(place)
    return JsonResponse([{'code':place.code, 'place':place.busstop, 'city':place.city, 'country': place.country} for place in filters], safe=False)

@csrf_exempt
def train(request):
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    trip_type = request.GET.get('TrainTripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        trainday2 = Week.objects.get(number=return_date.weekday()) ##
        origin2 = Railway.objects.get(code=d_place.upper())   ##
        destination2 = Railway.objects.get(code=o_place.upper())  ##
    seat = request.GET.get('SeatClass')

    trainday = Week.objects.get(number=depart_date.weekday())
    destination = Railway.objects.get(code=d_place.upper())
    origin = Railway.objects.get(code=o_place.upper())
    if seat == 'economy':
        trains = Train.objects.filter(depart_day=trainday,origin=origin,destination=destination).exclude(economy_fare=0).order_by('economy_fare')
        try:
            max_price = trains.last().economy_fare
            min_price = trains.first().economy_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            trains2 = Train.objects.filter(depart_day=trainday2,origin=origin2,destination=destination2).exclude(economy_fare=0).order_by('economy_fare')    ##
            try:
                max_price2 = trains2.last().economy_fare   ##
                min_price2 = trains2.first().economy_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##
                
    elif seat == 'business':
        trains = Train.objects.filter(depart_day=trainday,origin=origin,destination=destination).exclude(business_fare=0).order_by('business_fare')
        try:
            max_price = trains.last().business_fare
            min_price = trains.first().business_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            trains2 = Train.objects.filter(depart_day=trainday2,origin=origin2,destination=destination2).exclude(business_fare=0).order_by('business_fare')    ##
            try:
                max_price2 = trains2.last().business_fare   ##
                min_price2 = trains2.first().business_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##

    elif seat == 'first':
        trains = Train.objects.filter(depart_day=trainday,origin=origin,destination=destination).exclude(first_fare=0).order_by('first_fare')
        try:
            max_price = trains.last().first_fare
            min_price = trains.first().first_fare
        except:
            max_price = 0
            min_price = 0
            
        if trip_type == '2':    ##
            trains2 = Train.objects.filter(depart_day=trainday2,origin=origin2,destination=destination2).exclude(first_fare=0).order_by('first_fare')
            try:
                max_price2 = trains2.last().first_fare   ##
                min_price2 = trains2.first().first_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##    ##
    print(trains)
    #print(calendar.day_name[depart_date.weekday()])
    if trip_type == '2':
        return render(request, "travel/search_train.html", {
            'trains': trains,
            'origin': origin,
            'destination': destination,
            'trains2': trains2,   ##
            'origin2': origin2,    ##
            'destination2': destination2,    ##
            'seat': seat.capitalize(),
            'train_trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100,
            'max_price2': math.ceil(max_price2/100)*100,    ##
            'min_price2': math.floor(min_price2/100)*100    ##
        })
    else:
        return render(request, "travel/search_train.html", {
            'trains': trains,
            'origin': origin,
            'destination': destination,
            'seat': seat.capitalize(),
            'train_trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100
        })

@csrf_exempt
def bus(request):
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    trip_type = request.GET.get('BusTripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        busday2 = Week.objects.get(number=return_date.weekday()) ##
        origin2 = Busstop.objects.get(code=d_place.upper())   ##
        destination2 = Busstop.objects.get(code=o_place.upper())  ##
    seat = request.GET.get('SeatClass')

    busday = Week.objects.get(number=depart_date.weekday())
    destination = Busstop.objects.get(code=d_place.upper())
    origin = Busstop.objects.get(code=o_place.upper())
    if seat == 'economy':
        buses = Bus.objects.filter(depart_day=busday,origin=origin,destination=destination).exclude(economy_fare=0).order_by('economy_fare')
        try:
            max_price = buses.last().economy_fare
            min_price = buses.first().economy_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            buses2 = Bus.objects.filter(depart_day=busday2,origin=origin2,destination=destination2).exclude(economy_fare=0).order_by('economy_fare')    ##
            try:
                max_price2 = buses2.last().economy_fare   ##
                min_price2 = buses2.first().economy_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##
                
    elif seat == 'business':
        buses = Bus.objects.filter(depart_day=busday,origin=origin,destination=destination).exclude(business_fare=0).order_by('business_fare')
        try:
            max_price = buses.last().business_fare
            min_price = buses.first().business_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            buses2 = Bus.objects.filter(depart_day=busday2,origin=origin2,destination=destination2).exclude(business_fare=0).order_by('business_fare')    ##
            try:
                max_price2 = buses2.last().business_fare   ##
                min_price2 = buses2.first().business_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##

    elif seat == 'first':
        buses = Bus.objects.filter(depart_day=busday,origin=origin,destination=destination).exclude(first_fare=0).order_by('first_fare')
        try:
            max_price = buses.last().first_fare
            min_price = buses.first().first_fare
        except:
            max_price = 0
            min_price = 0
            
        if trip_type == '2':    ##
            buses2 = Bus.objects.filter(depart_day=busday2,origin=origin2,destination=destination2).exclude(first_fare=0).order_by('first_fare')
            try:
                max_price2 = buses2.last().first_fare   ##
                min_price2 = buses2.first().first_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##    ##
    #print(calendar.day_name[depart_date.weekday()])
    if trip_type == '2':
        return render(request, "travel/search_bus.html", {
            'buses': buses,
            'origin': origin,
            'destination': destination,
            'buses2': buses2,   ##
            'origin2': origin2,    ##
            'destination2': destination2,    ##
            'seat': seat.capitalize(),
            'bus_trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100,
            'max_price2': math.ceil(max_price2/100)*100,    ##
            'min_price2': math.floor(min_price2/100)*100    ##
        })
    else:
        return render(request, "travel/search_bus.html", {
            'buses': buses,
            'origin': origin,
            'destination': destination,
            'seat': seat.capitalize(),
            'bus_trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100
        })

def review_bus(request):
    bus_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    booktype = request.GET.get('booktype')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        bus_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        bus1 = Bus.objects.get(id=bus_1)
        bus1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),bus1.depart_time.hour,bus1.depart_time.minute)
        bus1adate = (bus1ddate + bus1.duration)
        bus2 = None
        bus2ddate = None
        bus2adate = None
        if round_trip:
            bus2 = Bus.objects.get(id=bus_2)
            bus2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),bus2.depart_time.hour,bus2.depart_time.minute)
            bus2adate = (bus2ddate + bus2.duration)
        #print("//////////////////////////////////")
        #print(f"bus1ddate: {bus1adate-bus1ddate}")
        #print("//////////////////////////////////")
        if round_trip:
            return render(request, "travel/book.html", {
                'flight1': bus1,
                'flight2': bus2,
                "flight1ddate": bus1ddate,
                "flight1adate": bus1adate,
                "flight2ddate": bus2ddate,
                "flight2adate": bus2adate,
                "seat": seat,
                "fee": FEE,
                "booktype": booktype,
            })
        return render(request, "travel/book.html", {
            'flight1': bus1,
            "flight1ddate": bus1ddate,
            "flight1adate": bus1adate,
            "seat": seat,
            "fee": FEE,
            "booktype": booktype,
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def review_train(request):
    train_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    booktype = request.GET.get('booktype')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        train_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        train1 = Train.objects.get(id=train_1)
        train1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),train1.depart_time.hour,train1.depart_time.minute)
        train1adate = (train1ddate + train1.duration)
        train2 = None
        train2ddate = None
        train2adate = None
        if round_trip:
            train2 = Train.objects.get(id=train_2)
            train2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),train2.depart_time.hour,train2.depart_time.minute)
            train2adate = (train2ddate + train2.duration)
        #print("//////////////////////////////////")
        #print(f"train1ddate: {train1adate-train1ddate}")
        #print("//////////////////////////////////")
        if round_trip:
            return render(request, "travel/book.html", {
                'flight1': train1,
                'flight2': train2,
                "flight1ddate": train1ddate,
                "flight1adate": train1adate,
                "flight2ddate": train2ddate,
                "flight2adate": train2adate,
                "seat": seat,
                "fee": FEE,
                "booktype": booktype,
            })
        return render(request, "travel/book.html", {
            'flight1': train1,
            "flight1ddate": train1ddate,
            "flight1adate": train1adate,
            "seat": seat,
            "fee": FEE,
            "booktype": booktype,
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def book_train(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            train_1 = request.POST.get('flight1')
            train_1date = request.POST.get('flight1Date')
            train_1class = request.POST.get('flight1Class')
            booktype = request.POST.get('booktype')
            f2 = False
            if request.POST.get('flight2'):
                train_2 = request.POST.get('flight2')
                train_2date = request.POST.get('flight2Date')
                train_2class = request.POST.get('flight2Class')
                f2 = True
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            train1 = Train.objects.get(id=train_1)
            if f2:
                train2 = Train.objects.get(id=train_2)
            passengerscount = request.POST['passengersCount']
            passengers=[]
            for i in range(1,int(passengerscount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,gender=gender.lower()))
            coupon = request.POST.get('coupon')
            
            try:
                ticket1 = createTrainticket(request.user,passengers,passengerscount,train1,train_1date,train_1class,coupon,countrycode,email,mobile)
                if f2:
                    ticket2 = createTrainticket(request.user,passengers,passengerscount,train2,train_2date,train_2class,coupon,countrycode,email,mobile)

                if(train_1class == 'Economy'):
                    if f2:
                        fare = (train1.economy_fare*int(passengerscount))+(train2.economy_fare*int(passengerscount))
                    else:
                        fare = train1.economy_fare*int(passengerscount)
                elif (train_1class == 'Business'):
                    if f2:
                        fare = (train1.business_fare*int(passengerscount))+(train2.business_fare*int(passengerscount))
                    else:
                        fare = train1.business_fare*int(passengerscount)
                elif (train_1class == 'First'):
                    if f2:
                        fare = (train1.first_fare*int(passengerscount))+(train2.first_fare*int(passengerscount))
                    else:
                        fare = train1.first_fare*int(passengerscount)
            except Exception as e:
                return HttpResponse(e)
            

            if f2:    ##
                return render(request, "travel/payment.html", { ##
                    'fare': fare+FEE,   ##
                    'ticket': ticket1.id,   ##
                    'ticket2': ticket2.id,
                    'booktype': booktype   ##
                })  ##
            return render(request, "travel/payment.html", {
                'fare': fare+FEE,
                'ticket': ticket1.id,
                'booktype': booktype
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def book_bus(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            bus_1 = request.POST.get('flight1')
            bus_1date = request.POST.get('flight1Date')
            bus_1class = request.POST.get('flight1Class')
            booktype = request.POST.get('booktype')
            f2 = False
            if request.POST.get('flight2'):
                bus_2 = request.POST.get('flight2')
                bus_2date = request.POST.get('flight2Date')
                bus_2class = request.POST.get('flight2Class')
                f2 = True
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            bus1 = Bus.objects.get(id=bus_1)
            if f2:
                bus2 = Bus.objects.get(id=bus_2)
            passengerscount = request.POST['passengersCount']
            passengers=[]
            for i in range(1,int(passengerscount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,gender=gender.lower()))
            coupon = request.POST.get('coupon')
            
            try:
                ticket1 = createBusticket(request.user,passengers,passengerscount,bus1,bus_1date,bus_1class,coupon,countrycode,email,mobile)
                if f2:
                    ticket2 = createBusticket(request.user,passengers,passengerscount,bus2,bus_2date,bus_2class,coupon,countrycode,email,mobile)

                if(bus_1class == 'Economy'):
                    if f2:
                        fare = (bus1.economy_fare*int(passengerscount))+(bus2.economy_fare*int(passengerscount))
                    else:
                        fare = bus1.economy_fare*int(passengerscount)
                elif (bus_1class == 'Business'):
                    if f2:
                        fare = (bus1.business_fare*int(passengerscount))+(bus2.business_fare*int(passengerscount))
                    else:
                        fare = bus1.business_fare*int(passengerscount)
                elif (bus_1class == 'First'):
                    if f2:
                        fare = (bus1.first_fare*int(passengerscount))+(bus2.first_fare*int(passengerscount))
                    else:
                        fare = bus1.first_fare*int(passengerscount)
            except Exception as e:
                return HttpResponse(e)
            

            if f2:    ##
                return render(request, "travel/payment.html", { ##
                    'fare': fare+FEE,   ##
                    'ticket': ticket1.id,   ##
                    'ticket2': ticket2.id,
                    'booktype': booktype   ##
                })  ##
            return render(request, "travel/payment.html", {
                'fare': fare+FEE,
                'ticket': ticket1.id,
                'booktype': booktype
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST['ticket']
            booktype = request.POST.get('booktype')
            t2 = False
            if request.POST.get('ticket2'):
                ticket2_id = request.POST['ticket2']
                t2 = True
            fare = request.POST.get('fare')
            card_number = request.POST['cardNumber']
            card_holder_name = request.POST['cardHolderName']
            exp_month = request.POST['expMonth']
            exp_year = request.POST['expYear']
            cvv = request.POST['cvv']

            try:
                if booktype == 'book_bus':
                    ticket = BusTicket.objects.get(id=ticket_id)
                elif booktype == 'book_train':
                    ticket = TrainTicket.objects.get(id=ticket_id)
                ticket.status = 'CONFIRMED'
                ticket.booking_date = datetime.now()
                ticket.save()
                if t2:
                    if booktype == 'book_bus':
                        ticket2 = BusTicket.objects.get(id=ticket2_id)
                    elif booktype == 'book_train':
                        ticket2 = TrainTicket.objects.get(id=ticket2_id)
                    ticket2.status = 'CONFIRMED'
                    ticket2.save()
                    return render(request, 'travel/payment_process.html', {
                        'ticket1': ticket,
                        'ticket2': ticket2,
                        'booktype': booktype,
                    })
                return render(request, 'travel/payment_process.html', {
                    'ticket1': ticket,
                    'ticket2': "",
                    'booktype': booktype,
                })
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, booktype, ref):

    if booktype == "book_bus":
        ticket = BusTicket.objects.get(ref_no=ref)
        return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.bus.origin.code,
        'to': ticket.bus.destination.code,
        'flight_date': ticket.bus_ddate,
        'status': ticket.status
    })
        
        
    elif booktype == "book_train":
        ticket = TrainTicket.objects.get(ref_no=ref)
        return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.train.origin.code,
        'to': ticket.train.destination.code,
        'flight_date': ticket.train_ddate,
        'status': ticket.status
    })

    

@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    booktype = request.GET.get("booktype")
    if BusTicket.objects.filter(ref_no=ref).exists():
        ticket1 = BusTicket.objects.get(ref_no=ref)
    elif TrainTicket.objects.filter(ref_no=ref).exists():
        ticket1 = TrainTicket.objects.get(ref_no=ref)
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year,
        'booktype': booktype,
    }
    pdf = render_to_pdf('travel/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def bookings(request):
    if request.user.is_authenticated:
        tickets1 = TrainTicket.objects.filter(user=request.user).order_by('-booking_date')
        tickets2 = BusTicket.objects.filter(user=request.user).order_by('-booking_date')
        tickets = list(chain(tickets1, tickets2))
        return render(request, 'travel/bookings.html', {
            'page': 'bookings',
            'tickets': tickets
        })
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            try:
                if BusTicket.objects.filter(ref_no=ref).exists():
                    ticket = BusTicket.objects.get(ref_no=ref)
                elif TrainTicket.objects.filter(ref_no=ref).exists():
                    ticket = TrainTicket.objects.get(ref_no=ref)  
                if ticket.user == request.user:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")

def resume_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            if BusTicket.objects.filter(ref_no=ref).exists():
                ticket = BusTicket.objects.get(ref_no=ref)
                booktype = 'book_bus'
            elif TrainTicket.objects.filter(ref_no=ref).exists():
                ticket = TrainTicket.objects.get(ref_no=ref)
                booktype = 'book_train' 
            if ticket.user == request.user:
                return render(request, "travel/payment.html", {
                    'fare': ticket.total_fare,
                    'ticket': ticket.id,
                    'booktype': booktype,
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

def contact(request):
    return render(request, 'travel/contact.html')

def privacy_policy(request):
    return render(request, 'travel/privacy-policy.html')

def terms_and_conditions(request):
    return render(request, 'travel/terms.html')

def about_us(request):
    return render(request, 'travel/about.html')