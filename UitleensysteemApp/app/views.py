from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from app.models import *
from datetime import datetime
from app.utils import *
import copy

# Create your views here.


def signin(request):
    #check of user is ingelogd en redirect naar overview, geen nut om opnieuw in te loggen
    if request.user.is_authenticated:
        return render(request, 'app/overview.html')
    return render(request, 'app/signin.html')

def signup(request):
    return render(request, 'app/signup.html')

def overview(request):
    now=datetime.now()
    time = now.strftime("%Y-%m")
    chosen_month_and_year = ""

    if request.method == "POST":
        time = request.POST.get('time')
        timeDateTime = datetime.strptime(str(time), "%Y-%m")
        chosen_month = timeDateTime.month
        chosen_year = timeDateTime.year
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
        #check of het admin is en skip rendering
        if calendar_event.calendarid.userid.username == "Admin":
            continue


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

        rgb = hash_to_rgb(calendar_event, "dark", 34, 21, 45)
        #calender_event is de key dat als object wordt meegegeven
        calendar_event_dictionary[calendar_event] = {'event_days_as_set': event_days_as_set, 'rgb': rgb}

    
    print(calendar_event_dictionary)
    #print(days_in_chosen_month_as_set)
    return render(request, 'app/overview.html', {
        'time': time,
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

        #skip admin rendering
        admin = get_object_or_404(User, username="Admin")
        admin_calendar = get_object_or_404(Calendar, userid=admin)
        users = User.objects.exclude(username='Admin')
        calendar_events = CalendarEvent.objects.exclude(calendarid=admin_calendar)

        event_types = EventType.objects.all()
        #print(calendar_events)
        # event CRUD handling
        if request.method == "POST":
            event_id = request.POST.get('event_id')
            calendar_event_id = request.POST.get('calendar_event_id')
            #print(calendar_event_id)

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
                event_temp = copy.deepcopy(event)

                calendarid = get_object_or_404(Calendar, userid=userid)
                #print(calendar_event_id)
                #print(CalendarEvent.objects.filter(id=calendar_event_id).exists())
                calendar_event = get_object_or_404(CalendarEvent, id=calendar_event_id)
                calendar_event_temp = copy.deepcopy(calendar_event)
                #print(f"Event: {event}, Event ID: {event_id}, Action: {action}, event_type: {event_type}, Start Date: {start_date}, End Date: {end_date}")                
                event.start = start_date
                event.end = end_date
                event.itemid = get_object_or_404(Item, naam=item_naam)
                # Check eventtype object of object ook echt bestaat met de gegeven event_type
                event.eventType = get_object_or_404(EventType, type=event_type)

                # Default checked Django models.Model implementatie dus de ids van de object, 
                # maar ik vergelijk de string representatie van de class die dus een stringrepresentatie bevat van de inhoud 
                user = get_object_or_404(User, username=user_username)
                userCalendar = get_object_or_404(Calendar, userid=user)
                calendar_event.calendarid = userCalendar
                print(str(event) == str(event_temp), str(calendar_event) == str(calendar_event_temp))
                if (str(event) == str(event_temp) and str(calendar_event) == str(calendar_event_temp)):
                    print("1", event, "and", event_temp)
                    messages.warning(request, "No changes detected from the updated event") 
                else:
                    print("2", str(event), str(event_temp))
                    checked = check_overlap(event)
                    if checked['overlap_flag']==False:
                        event.save()

                        calendar_event.save()

                        admin = get_object_or_404(User, username="Admin")
                        admin_calendar = get_object_or_404(Calendar, userid=admin)
                        admin_calendar_event = get_object_or_404(CalendarEvent, eventid=event_id, calendarid=admin_calendar)

                        admin_calendar_event.save()

                        messages.success(request, 'Event updated successfully.')
                    else:
                        messages.error(request, checked['warning'])

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


                #print(start, end)
                #een item kan meer aan een persoon uitgeleend worden, check of item vrij is voor deze periode
                checked = check_overlap(new_event)
                if checked['overlap_flag']==False:
                    new_event.save()
                    calendarid = get_object_or_404(Calendar, userid=userid)
                    new_calender_event = CalendarEvent(calendarid=calendarid, eventid=new_event)
                    new_calender_event.save()

                    admin = get_object_or_404(User, username="Admin")
                    admin_calendar = get_object_or_404(Calendar, userid=admin)
                    if not CalendarEvent.objects.filter(calendarid=admin_calendar, eventid=new_event).exists():
                        print("ook aan admin kalender toegevoegd")

                        new_calender_event = CalendarEvent(calendarid=admin_calendar, eventid=new_event)
                        new_calender_event.save()

                    messages.success(request, f"Event successfully added from {checked['start_new_event'].date()} till {checked['start_new_event'].date()}")
                    #update calendar_events met nieuw object om mee te geven aan render
                    calendar_events = CalendarEvent.objects.exclude(calendarid=admin_calendar)
                    #print(new_calender_event)
                else:
                    messages.error(request, checked['warning'])
                return render(request, 'app/event-manager.html', {
                    'calendar_events': calendar_events,
                    'event_types': event_types,
                    'items': items,
                    'users': users,
                    "event_id": event_id, 
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

def user_manager(request):
    #check of user is ingelogd
    if request.user.is_authenticated:
        #alle objecten van model van models.py
        users = User.objects.exclude(username='Admin')

        #print(calendar_events)
        # event CRUD handling
        if request.method == "POST":
            action = request.POST.get('action')
            
            #todo: check eerst of data niet leeg is en geldig is met database opties
            user_id = request.POST.get('user_id')
            user_username = request.POST.get('user_username')
            user_first_name = request.POST.get('user_first_name')
            user_last_name = request.POST.get('user_last_name')
            user_password = request.POST.get('user_password')
            user_password_check = request.POST.get('user_password_check')
            user_email = user_username


            if action == "Update":
                user = get_object_or_404(User, id=user_id)
                user_temp = copy.deepcopy(user)

                print(user_username)

                try:
                    validate_email(user_username)
                    #Validate_email van validators gooit een error, geen boolean, dus error handling moet gebeuren
                except ValidationError:
                    messages.warning(request, 'Invalid email address.')
                    return render(request, 'app/user-manager.html', {
                        'user_username': user_username,
                        'user_first_name': user_first_name,
                        'user_last_name': user_last_name,
                        'user_email' : user_email,
                        'users': users
                    })
                user.username = user_username
                user.first_name = user_first_name
                user.last_name = user_last_name
                user.email = user_email
                if user_password:
                    user.set_password(user_password)

                # Default checked Django models.Model implementatie dus de ids van de object, 
                # maar ik vergelijk de string representatie van de class die dus een stringrepresentatie bevat van de inhoud 
                if (str(user) == str(user_temp)):
                    print("1", user, "and", user_temp)
                    messages.warning(request, "No changes detected from the updated event") 
                else:
                    #print("2", event, event_temp)
                    user.save()
                    
                    messages.success(request, 'User updated successfully.')

            elif action == 'Delete':
                # Delete the event
                user = get_object_or_404(User, id=user_id)
                user.delete()

                messages.success(request, 'User deleted successfully.')

            elif action == 'Create':
                if not all([user_first_name, user_last_name, user_email, user_password, user_password_check]):
                    messages.warning(request, 'Error missing fields.')
                    return render(request, 'app/user-manager.html', {
                        'user_username': user_username,
                        'user_first_name': user_first_name,
                        'user_last_name': user_last_name,
                        'user_email' : user_email,
                        'users': users,

                    })
                        
                #Email validatie met Django email validator
                try:
                    validate_email(user_email)
                    #Validate_email van validators gooit een error, geen boolean, dus error handling moet gebeuren
                except ValidationError:
                    messages.warning(request, 'Invalid email address.')
                    return render(request, 'app/user-manager.html', {
                        'user_username': user_username,
                        'user_first_name': user_first_name,
                        'user_last_name': user_last_name,
                        'user_email' : user_email,
                        'users': users,
                    })

                #Check paswoord ook hetzelfde is
                if user_password == user_password_check:
                    User.objects.create_user(username=user_username, email=user_email, password=user_password, first_name=user_first_name, last_name=user_last_name)
                    user = get_object_or_404(User, username=user_username)

                    calendar = Calendar(userid=user, description=user.username)
                    calendar.save()
                    messages.success(request, "successfully added user")
                else:
                    messages.warning(request, "Password doesn't match.")
                    return render(request, 'app/user-manager.html', {
                        'user_username': user_username,
                        'user_first_name': user_first_name,
                        'user_last_name': user_last_name,
                        'user_email' : user_email,
                        'users': users,
                    })

                #update users met nieuw object om mee te geven aan render
                users = CalendarEvent.objects.all()
                #print(new_calender_event)
                return render(request, 'app/user-manager.html', {
                    'user_username': user_username,
                    'user_first_name': user_first_name,
                    'user_last_name': user_last_name,
                    'user_email' : user_email,
                    'users': users,
                })

        #Geef data door aan event manager view
        return render(request, 'app/user-manager.html', {
            'users': users
            })
    else:
        return render(request, 'app/user-manager.html')

def item_manager(request):
    #check of user is ingelogd
    if request.user.is_authenticated:

        #alle objecten van model van models.py
        items = Item.objects.all()
        item_types = ItemType.objects.all()

        #print(calendar_events)
        # event CRUD handling
        if request.method == "POST":
            action = request.POST.get('action')
            
            #todo: check eerst of data niet leeg is en geldig is met database opties
            item_id = request.POST.get('item_id')
            item_naam = request.POST.get('item_naam')
            item_beschrijving = request.POST.get('item_beschrijving')
            item_type = request.POST.get('item_type')

            if action == "Update":
                item = get_object_or_404(Item, id=item_id)
                item_temp = copy.deepcopy(item)

                print(item_naam)
                enforced_item_name = enforce_item_name(item_naam)

                item.naam = enforced_item_name
                item.beschrijving = item_beschrijving
                item.itemTypeID = get_object_or_404(ItemType, type=item_type)

                # Default checked Django models.Model implementatie dus de ids van de object, 
                # maar ik vergelijk de string representatie van de class die dus een stringrepresentatie bevat van de inhoud 
                if (str(item) == str(item_temp)):
                    print("1", item, "and", item_temp)
                    messages.warning(request, "No changes detected from the updated event") 
                else:
                    #print("2", event, event_temp)
                    item.save()
                    
                    messages.success(request, 'Item updated successfully.')

            elif action == 'Delete':
                # Delete the item
                item = get_object_or_404(Item, id=item_id)
                item.delete()

                messages.success(request, 'Item deleted successfully.')

            elif action == 'Create':
                if not all([item_naam, item_beschrijving]):
                    messages.warning(request, 'Error missing fields.')
                    return render(request, 'app/item-manager.html', {
                        'item_id' : item_id,
                        'item_naam': item_naam,
                        'item_beschrijving': item_beschrijving,
                        'item_type' : item_type,
                        'items': items,
                        'item_types' : item_types
                    })
                item_itemTypeID = get_object_or_404(ItemType, type=item_type)
                enforced_item_name = enforce_item_name(item_naam)
                #check of item al bestaat met filter() en exists() van Django
                if not Item.objects.filter(naam=enforced_item_name).exists():
                    new_item = Item(naam=enforced_item_name, beschrijving=item_beschrijving, itemTypeID=item_itemTypeID)
                    new_item.save()
                    messages.success(request, "successfully added item")
                else:
                    messages.error(request, f"Item already exists when parsing your item name in our enforced format, resulting in: \"{enforced_item_name}\"")


                #update items met nieuw object om mee te geven aan render
                items = Item.objects.all()
                #print(new_calender_event)
                return render(request, 'app/item-manager.html', {
                    'item_id' : item_id,
                    'item_naam': item_naam,
                    'item_beschrijving': item_beschrijving,
                    'item_type' : item_type,
                    'items': items,
                    'item_types' : item_types
                })

        #Geef data door aan event manager view
        return render(request, 'app/item-manager.html', {
            'items': items,
            'item_types' : item_types
            })
    else:
        return render(request, 'app/item-manager.html')

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
        messages.success(request, "successfully registered, please login.")
        return render(request, 'app/signin.html', {'firstname': firstname, 'lastname': lastname, 'email': email})
    else:
        messages.warning(request, "Password doesn't match.")
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('signin')
