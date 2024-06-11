from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from app.models import *
from datetime import datetime
import calendar

# Create your views here.


def signin(request):
    #check of user is ingelogd en redirect naar overview, geen nut om opnieuw in te loggen
    if request.user.is_authenticated:
        return render(request, 'app/overview.html')
    return render(request, 'app/signin.html')

def signup(request):
    return render(request, 'app/signup.html')

def overview(request):
    allCalendarEvents = CalendarEvent.objects.all()
    currentDateTime = datetime.now()
    currentYear = currentDateTime.year
    currentMonth = currentDateTime.month

    # Month in text 
    currentMonthInText = currentDateTime.strftime("%B")
    currentYearInText = currentDateTime.strftime("%Y")

    currentDate = currentDateTime.date()

    #voor de maan july returned 'daysInCurrentMonth = calendar.monthrange(currentYear, currentMonth)' dit: (5, 30) 
    #30 is het aantal dagen voor de huidige maand nodig voor de kalender generatie daarom de [1] positie van de array aka tuple
    daysInCurrentMonth = calendar.monthrange(currentYear, currentMonth)[1]
    listDaysInCurrentMonth = list(range(1, daysInCurrentMonth+1))
    #print(f"{daysInCurrentMonth}")
    #check events van calendarEvent voor de huidige maand:
    calenderEventDictionary = {}
    for calendarEvent in allCalendarEvents:

        #strptime vraag string aan geen object daarom str() dan .month om enkel de converted maand over te houden
        startDateTimeObjectOfCalendarEvent = datetime.strptime(str(calendarEvent.eventid.start), "%Y-%m-%d")
        endDateTimeObjectOfCalendarEvent = datetime.strptime(str(calendarEvent.eventid.end), "%Y-%m-%d")

        calenderEventStartMonth = startDateTimeObjectOfCalendarEvent.month
        startDay = int(startDateTimeObjectOfCalendarEvent.day)
        endDay = int(endDateTimeObjectOfCalendarEvent.day)

        #print(f"{calenderEventStartMonthString} and {currentMonth}")

        if calenderEventStartMonth == currentMonth:
            #check of enddate ook in maand zit anders einde dag van de maand
            if endDateTimeObjectOfCalendarEvent.month != currentMonth:
                listDaysTillEndOfMonth = list(range(startDay, daysInCurrentMonth+1))
                calenderEventDictionary[calendarEvent] = listDaysTillEndOfMonth
            # Generate and return the list of days
            else:
                listDaysTillEndDate = list(range(startDay, endDay + 1))
                calenderEventDictionary[calendarEvent] = listDaysTillEndDate
    
    print(calenderEventDictionary)
    print(listDaysInCurrentMonth)
    return render(request, 'app/overview.html', {
        "calenderEventDictionary": calenderEventDictionary, 
        "listDaysInCurrentMonth": listDaysInCurrentMonth, 
        "currentMonthInText":currentMonthInText,
        "currentYearInText": currentYearInText
        })

def event_manager(request):
    #check of user is ingelogd
    if request.user.is_authenticated:

        # event CRUD handling
        if request.method == "POST":
            eventID = request.POST.get('event_id')
            action = request.POST.get('action')
            event = get_object_or_404(Event, id=eventID)
            print(f"{event.id} en {eventID} en {action}")


            if action == "Update":
                #todo: check eerst of data niet leeg is en geldig is met database opties
                eventType = request.POST.get('event_type')
                item_naam = request.POST.get('item_naam')
                startDate = request.POST.get('start_date')
                endDate = request.POST.get('end_date')

                #print(f"Event: {event}, Event ID: {eventID}, Action: {action}, EventType: {eventType}, Start Date: {startDate}, End Date: {endDate}")
                
                #check of endDate niet voor startDate komt
                if startDate>=endDate:
                    messages.warning(request, f"Dates are incorrect: {endDate} is before {startDate}") 
                else:
                    event.start = startDate
                    event.end = endDate
                    event.itemid = get_object_or_404(Item, naam=item_naam)
                    # Check eventtype object of object ook echt bestaat met de gegeven eventType
                    event.eventType = get_object_or_404(EventType, type=eventType)
                    
                    event.save()
                    messages.success(request, 'Event updated successfully.')

            elif action == 'Delete':
                # Delete the event
                event.delete()
                messages.success(request, 'Event deleted successfully.')
        
        #alle objecten van model van models.py
        Items = Item.objects.all()
        CalendarEvents = CalendarEvent.objects.all()
        EventTypes = EventType.objects.all()

        #Geef data door aan event manager view
        return render(request, 'app/event-manager.html', {'calendarEvents': CalendarEvents, 'EventTypes': EventTypes, 'Items': Items})
    else:
        return render(request, 'app/event-manager.html')


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return redirect('overview')
    else:
        messages.warning(request, 'Wrong credentials.')
        return render(request, 'app/signin.html', {'username' : username})

def register(request):
    #POST is een dictionary object, POST.get(key, default=None) is hetzelfda als QueryDict.get(key, default=None)
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    password = request.POST.get("password")
    email = request.POST.get("email")
    passwordCheck = request.POST.get("passwordCheck")

    #Check of alle values ingevuld zijn met all() dit filtered ook None values eruit van QueryDict.get(key, default=None) anders error message
    if not all([firstname, lastname, email, password, passwordCheck]):
        messages.warning(request, 'Error missing fields.')
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})
    
    #Email validatie met Django email validator
    try:
        validate_email(email)
        #Validate_email van validators gooit een error, geen boolean, dus error handling moet gebeuren
    except ValidationError:
        messages.warning(request, 'Invalid email address.')
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})

    #Check paswoord ook hetzelfde is
    if password == passwordCheck:
        User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        messages.warning(request, "Succesfully registered, please login.")
        return render(request, 'app/signin.html', {'firstname': firstname, 'lastname': lastname, 'email': email})
    else:
        messages.warning(request, "Password doesn't match.")
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('signin')
