from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from app.models import *
from datetime import datetime
from app.utils import *

# Create your views here.


def signin(request):
    #check of user is ingelogd en redirect naar overview, geen nut om opnieuw in te loggen
    if request.user.is_authenticated:
        return render(request, 'app/overview.html')
    return render(request, 'app/signin.html')

def signup(request):
    return render(request, 'app/signup.html')

def overview(request):
    chosen_month_and_year = ""

    if request.method == "POST":
        chosen_month = request.POST.get('chosen_month')
        chosen_year = request.POST.get('chosen_year')
        chosen_month_and_year = {'month': chosen_month, 'year': chosen_year}

    all_calendar_events = CalendarEvent.objects.all()

    #chosen_month_and_year in this format {'month': 6, 'year': 2024}
    processed_calendar = process_calendar(chosen_month_and_year)

    chosen_month = processed_calendar.get('chosen_month')
    processed_calendar.get('chosen_months_year')
    chosen_month_to_text = processed_calendar.get('chosen_month_to_text')
    chosen_months_year_to_text = processed_calendar.get('chosen_months_year_to_text')
    days_in_chosen_month = processed_calendar.get('days_in_chosen_month')
    days_in_chosen_month_as_set = processed_calendar.get('days_in_chosen_month_as_set')

    #deze code block zal een {<calenderEventobject instance1>, {2,3,4,5}}
    calendar_event_dictionary = {}
    for calendar_event in all_calendar_events:
        #strptime vraagt string aan, geen object daarom str() dan .month om enkel de converted maand over te houden
        start_date_time_object_of_calendar_event = datetime.strptime(str(calendar_event.eventid.start), "%Y-%m-%d")
        end_date_time_object_of_calendar_event = datetime.strptime(str(calendar_event.eventid.end), "%Y-%m-%d")

        calendar_event_start_month = start_date_time_object_of_calendar_event.month
        calendar_event_end_month = end_date_time_object_of_calendar_event.month
        start_day = int(start_date_time_object_of_calendar_event.day)
        end_day = int(end_date_time_object_of_calendar_event.day)

        #print(f"{calenderEventStartMonthString} and {chosen_month}")
        #elifs zijn meer cpu efficient anders checkt deze door elke case, ookal is event_days_as_set al ingevuld
        if calendar_event_start_month == chosen_month and calendar_event_end_month == chosen_month:
            event_days_as_set = set(range(start_day, end_day + 1))
        elif calendar_event_start_month == chosen_month and calendar_event_end_month > chosen_month:
            event_days_as_set = set(range(start_day, days_in_chosen_month + 1))
        elif calendar_event_start_month < chosen_month and calendar_event_end_month == chosen_month:
            event_days_as_set = set(range(1, end_day + 1))
        elif calendar_event_start_month < chosen_month and calendar_event_end_month > chosen_month:
            event_days_as_set = set(range(1, days_in_chosen_month + 1))
        else:
            event_days_as_set = {}

        rgb = hash_to_rgb(calendar_event, "dark", 75, 28, 82)
        #calender_event is de key dat als object wordt meegegeven
        calendar_event_dictionary[calendar_event] = {'event_days_as_set': event_days_as_set, 'rgb': rgb}

    
    print(calendar_event_dictionary)
    #print(days_in_chosen_month_as_set)
    return render(request, 'app/overview.html', {
        "calendar_event_dictionary": calendar_event_dictionary, 
        "days_in_chosen_month_as_set": days_in_chosen_month_as_set, 
        "chosen_month_to_text":chosen_month_to_text,
        "chosen_months_year_to_text": chosen_months_year_to_text
        })

def event_manager(request):
    #check of user is ingelogd
    if request.user.is_authenticated:
        #alle objecten van model van models.py
        items = Item.objects.all()
        users = User.objects.all()
        calendar_events = CalendarEvent.objects.all()
        event_types = EventType.objects.all()
        print(calendar_events)
        # event CRUD handling
        if request.method == "POST":
            event_id = request.POST.get('event_id')
            calendar_event_id = request.POST.get('calendar_event_id')
            action = request.POST.get('action')
            
            #todo: check eerst of data niet leeg is en geldig is met database opties
            event_type = request.POST.get('event_type')
            item_naam = request.POST.get('item_naam')
            user_username = request.POST.get('user_username')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
        
            userid = get_object_or_404(User, username=user_username)
            
            #print(f"{event.id} en {event_id} en {action}")
            #check of end_date niet voor start_date komt
            if start_date>=end_date:
                messages.warning(request, f"Dates are incorrect: {end_date} is before {start_date}") 
                
            elif action == "Update":
                event = get_object_or_404(Event, id=event_id)
                calendar_event = get_object_or_404(CalendarEvent, eventid=event_id)
                #print(f"Event: {event}, Event ID: {event_id}, Action: {action}, event_type: {event_type}, Start Date: {start_date}, End Date: {end_date}")                
                event.start = start_date
                event.end = end_date
                event.itemid = get_object_or_404(Item, naam=item_naam)
                # Check eventtype object of object ook echt bestaat met de gegeven event_type
                event.eventType = get_object_or_404(EventType, type=event_type)    
                event.save()

                
                calendar_event.calendarid = get_object_or_404(Calendar, userid=userid)
                calendar_event.save()

                messages.success(request, 'Event updated successfully.')

            elif action == 'Delete':
                # Delete the event
                event = get_object_or_404(Event, id=event_id)
                event.delete()

                messages.success(request, 'Event deleted successfully.')

            elif action == 'Create':
                eventType = get_object_or_404(EventType, type=event_type)
                itemid = get_object_or_404(Item, naam=item_naam)
                new_event = Event(eventType=eventType, itemid=itemid, start=start_date, end=end_date)
                #print(new_event)

                start_new_event =datetime.strptime(str(new_event.start), "%Y-%m-%d")
                end_new_event = datetime.strptime(str(new_event.end), "%Y-%m-%d")

                #print(start, end)
                #een item kan meer aan een persoon uitgeleend worden, check of item vrij is voor deze periode
                overlap_flag = False
                for calendar_event1 in calendar_events:
                    #check eerst of item hetzelfde is van calendar_event1 instance
                    if new_event.itemid == calendar_event1.eventid.itemid:
                        #print(new_event.itemid.naam, calendar_event1.eventid.itemid.naam)
                        start_old_event = datetime.strptime(str(calendar_event1.eventid.start), "%Y-%m-%d")
                        end_old_event = datetime.strptime(str(calendar_event1.eventid.end), "%Y-%m-%d")

                        print(start_new_event.day, end_new_event.day, "and", start_old_event.day, end_old_event.day)

                        if start_new_event <= end_old_event and end_new_event >= start_old_event:
                            if start_new_event >= start_old_event and end_new_event <= end_old_event:
                                print("Start en einddag lopen in periode van andere reservering")
                                messages.warning(request, "Start and end dates fall within the period of another reservation")
                                overlap_flag = True
                                break
                            elif start_new_event <= start_old_event and end_new_event >= end_old_event:
                                print("Start en einddag lopen over een periode van andere reservering")
                                messages.warning(request, "New event spans across the entire period of another reservation")
                                overlap_flag = True
                                break
                            elif start_new_event <= end_old_event and end_new_event >= start_old_event:
                                if start_new_event <= end_old_event:
                                    print("Startdag loopt in periode van andere reservering")
                                    messages.warning(request, "Start date overlaps with the period of another reservation")
                                else:
                                    print("Einddag loopt in periode van andere reservering")
                                    messages.warning(request, "End date overlaps with the period of another reservation")
                                
                                overlap_flag = True
                                break
                        else:
                            print("Geen overlap")

                if overlap_flag==False:
                    new_event.save()
                    calendarid = get_object_or_404(Calendar, userid=userid)
                    new_calender_event = CalendarEvent(calendarid=calendarid, eventid=new_event)
                    new_calender_event.save()

                    #update calendar_events met nieuw object om mee te geven aan render
                    calendar_events = CalendarEvent.objects.all()
                    #print(new_calender_event)
                return render(request, 'app/event-manager.html', {
                    'calendar_events': calendar_events,
                    'event_types': event_types,
                    'items': items,
                    'users': users,
                    "event_id": event_id, 
                    "calendar_event_id": calendar_event_id, 
                    "event_type": event_type, 
                    "item_naam": item_naam, 
                    "user_username": user_username, 
                    "start_date": start_date, 
                    "end_date": end_date
                    })

        #Geef data door aan event manager view
        return render(request, 'app/event-manager.html', {
            'calendar_events': calendar_events,
            'event_types': event_types,
            'items': items,
            'users': users
            })
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
    password_check = request.POST.get("password_check")

    #Check of alle values ingevuld zijn met all() dit filtered ook None values eruit van QueryDict.get(key, default=None) anders error message
    if not all([firstname, lastname, email, password, password_check]):
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
    if password == password_check:
        User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        user = get_object_or_404(User, username=email)
        calendar = Calendar(userid=user, description=user.username)
        calendar.save()
        messages.warning(request, "Succesfully registered, please login.")
        return render(request, 'app/signin.html', {'firstname': firstname, 'lastname': lastname, 'email': email})
    else:
        messages.warning(request, "Password doesn't match.")
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('signin')
