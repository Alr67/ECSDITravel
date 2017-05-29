from datetime import date

from PracticaECSDI.Constants import Constants


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
            if year < 2017 or year > Constants.maxYear:
                raise ValueError('Year must be between 2017 and ',Constants.maxYear,' ...')
            break
        except:
            pass
            print("Year must be between 2017 and ",Constants.maxYear," ...")
    return date(year,month,day)

def askForCity(response):
    while True:
        try:
            city = raw_input(response)
            city = city.strip()
            if city == 'Barcelona':
                return 'BCN'
            elif city == 'Paris':
                return 'CDG'
            elif city == 'Londres':
                return 'LGW'
            elif city == 'Madrid':
                return 'MAD'
            elif city == 'Estocolmo':
                return 'ARN'
            elif city == 'Milan':
                return 'MXP'
            else:
                raise ValueError('Not a valid city...')
            break
        except:
            pass
            print("Not a valid city...")

def askForCityLat(city):
    while True:
        try:
            if city == 'BCN':
                return 41.3887900
            elif city == 'CDG':
                return 48.8534100
            elif city == 'LGW':
                return 51.5085300
            elif city == 'MAD':
                return 40.4165000
            elif city == 'ARN':
                return 59.3325800
            elif city == 'MXP':
                return 45.4642700
            else:
                raise ValueError('Not a valid city...')
            break
        except:
            pass
            print("Not a valid city...")

def askForCityLong(city):
    while True:
        try:
            if city == 'BCN':
                return 2.1589900
            elif city == 'CDG':
                return 2.3488000
            elif city == 'LGW':
                return -0.1257400
            elif city == 'MAD':
                return -3.7025600
            elif city == 'ARN':
                return 18.0649000
            elif city == 'MXP':
                return 9.1895100
            else:
                raise ValueError('Not a valid city...')
            break
        except:
            pass
            print("Not a valid city...")