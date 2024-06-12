from datetime import datetime
import calendar
from app.models import *
import hashlib


def process_calendar(chosen_month_and_year):
    #chosen_month_and_year = {'month': 6, 'year': 2024}

    if chosen_month_and_year:
        month = chosen_month_and_year.get('month')
        year = chosen_month_and_year.get('year')
        
        #check of format correct is, anders exception
        if month is None or year is None:
            raise ValueError("De dictionary moet keys: 'month' & 'year' hebben, en de values: integers")
        
        #niewe datetime object met "jaar, maand, 1st dag"
        chosen_date_time = datetime(year, month, 1)
    else:
        chosen_date_time = datetime.now()

    chosen_month = chosen_date_time.month
    chosen_months_year = chosen_date_time.year

    # Month in text 
    chosen_month_to_text = chosen_date_time.strftime("%B")
    chosen_months_year_to_text = chosen_date_time.strftime("%Y")

    #voor de maan july returned 'days_in_chosen_month = calendar.monthrange(chosen_months_year, chosen_month)' dit: (5, 30) 
    #30 is het aantal dagen voor de huidige maand nodig voor de kalender generatie daarom de [1] positie van de array aka tuple
    days_in_chosen_month = calendar.monthrange(chosen_months_year, chosen_month)[1]
    days_in_chosen_month_as_set = set(range(1, days_in_chosen_month+1))

    #print(f"{daysInchosenMonth}")
    #check events van calendarEvent voor de huidige maand:

    return {
        'chosen_month': chosen_month,
        'chosen_months_year': chosen_months_year,
        'chosen_month_to_text': chosen_month_to_text,
        'chosen_months_year_to_text': chosen_months_year_to_text,
        'days_in_chosen_month': days_in_chosen_month,
        'days_in_chosen_month_as_set': days_in_chosen_month_as_set
    }

def hash_to_rgb(calendar_event: CalendarEvent, mode=None, offset_red=0, offset_green=0, offset_blue=0):
    #check of calendar_event is een instance van CalendarEvent
    if not isinstance(calendar_event, CalendarEvent):
        raise TypeError(f"calendar_event verwacht een CalendarEvent instance")
    
    #python hash is niet nuttig hier, verandert constant
    #daarom hashlib
    #https://docs.python.org/3/library/hashlib.html
    
    #md5 is sneller dan sha256 (output 128 bit vs 256 bit hash value)
    #calendar_event -> string versie ervan -> wordt dan encoded in hex -> wordt dan omgezet in een hexadecimal string.
    hash = hashlib.md5(str(calendar_event).encode()).hexdigest()

    #ik hoef geen abs() te gebruiken want int ziet deze byte hash als een unsigned integer aka enkele positieve natuurlijke getallen
    # int neemt hash als hexadecimale string aan met parameter 16 om het van hex naar een integer te brengen want 16 is gelijk aan 1 in hex
    rgb = int(hash, 16)

    

    #nu omzetten naar een value tussen 0-255 met modulo
    if mode == "bright":
        r = (rgb+offset_red) % 256
        g = (rgb*2+offset_green) % 256
        b = (rgb*3+offset_blue) % 256
    elif mode == "dark":
        r = (rgb+offset_red) % 128
        g = (rgb*2+offset_green) % 128
        b = (rgb*3+offset_blue) % 128
    elif mode == "very dark":
        r = (rgb+offset_red) % 64
        g = (rgb*2+offset_green) % 64
        b = (rgb*3+offset_blue) % 64
    else:
        raise TypeError(f"hash_to_rgb() verwacht een 2de parameter mode met ofwel \"bright\" of  \"dark\"")
    rgb = {'r': r, 'g': g, 'b': b}
    print(rgb)

    return rgb