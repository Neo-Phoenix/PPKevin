from datetime import datetime
import calendar


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