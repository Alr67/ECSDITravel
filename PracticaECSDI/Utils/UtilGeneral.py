from datetime import date

maxYear = 2020

def askForString(message):
    response = raw_input(message)
    while response.strip().find(" ") != -1:
        print "No puede contener espacios"
        response = raw_input(message)
        return response

def askForInt(message):
    while True:
        try:
            response = eval(raw_input(message))
            return response
        except:
            pass
            print("Not an integer value...")

def askForDate(message):
    print message
    day = 1
    month = 1
    year = 1
    while True:
        try:
            day = eval(raw_input("Day:"))
            if day < 1 or day > 30:
                raise ValueError('Day must be between 1 and 30 ...')
            break
        except:
            pass
            print("Day must be between 1 and 30 ...")
    while True:
        try:
            month = eval(raw_input("Month:"))
            if month < 1 or month > 12:
                raise ValueError('Month must be between 1 and 12 ...')
            break
        except:
            pass
            print("Month must be between 1 and 12 ...")

    while True:
        try:
            year = eval(raw_input("Year:"))
            if year < 2017 or year > maxYear:
                raise ValueError('Year must be between 2017 and ',maxYear,' ...')
            break
        except:
            pass
            print("Year must be between 2017 and ",maxYear," ...")
    return date(year,month,day)