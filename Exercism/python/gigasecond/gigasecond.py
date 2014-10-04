from datetime import date, timedelta

def add_gigasecond(date):
    seconds_in_day = 86400
    gigasecond = 10 ** 9
    days = int(gigasecond / seconds_in_day)
    seconds = gigasecond % seconds_in_day
    gigasecond = timedelta(days, seconds)
    
    return date + gigasecond
