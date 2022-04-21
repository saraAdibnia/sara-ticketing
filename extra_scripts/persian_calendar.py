from persiantools.jdatetime import JalaliDate
import datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint

# number_of_month=7 MEANS LAST 6 MONTH


def english_date_ranges(number_of_month=6):
    number_of_month -= 1 
    
    today_en = datetime.date.today()
    # 7 month earlier in english calendar
    earl_en = today_en - relativedelta(months=number_of_month)
    six_month_earlier_persian = JalaliDate(earl_en)
    result = []

    past_month = six_month_earlier_persian.month
    past_year = six_month_earlier_persian.year

    for i in range(number_of_month + 1):
        # turing the start of the persian month to a english calendar range
        range_1 = JalaliDate(past_year, past_month, 1).to_gregorian()

    # setting the end range
        # saving the persian month number for chart
        temp = {'persian_month': past_month}
        past_month += 1

        if past_month == 13:  # fixing the year number when reaches 12
            past_month = 1
            past_year += 1

        # turing the end  of the persian month to a english calendar range
        range_2 = JalaliDate(past_year, past_month,
                             1).to_gregorian() - relativedelta(days=1)
        temp['range_1'] = range_1
        temp['range_2'] = range_2
        if range_1 > today_en:
            continue
        result.append(temp)
    return result

# give all weeks with start and end days (datetime_format) based on persian calendar( start Week is Saturday and End is Frieday)
def persian_weeks_ranges(r1, r2):
    # r1, r2 = min(r1, r2), max(r1, r2)
    dif = r2- r1

    week_started = [r1 + datetime.timedelta(days = i) for i in range (dif.days + 1 )]

    ranges = [[s, s+datetime.timedelta(days= 6 )] for s in week_started if s.weekday() == 5]
    return ranges
# pprint(persian_weeks_ranges(datetime.date(2021,10,1), datetime.date(2021, 11, 2) ))



def en_month_period(number_of_month = 7 ):
    today = datetime.date.today().replace(day = 1) # first day of this month
    this_month = today.month
    this_year = today.year

    res = []
    n = number_of_month +1
    
    for i in range(0, number_of_month+1):
        rng1 = datetime.date(this_year, this_month, 1)

        if rng1.month == 1 :
            this_year -= 1
            this_month = 12
        else :
            this_month -=1 

        rng2 = datetime.date(this_year, this_month , 1  ) - relativedelta(day = 1)

        temp = {
            'english_month':rng1.month,
            'range_2':rng1, 
            'range_1': rng2
        }
        n -=1 
        res.append(temp)
    
    return res
