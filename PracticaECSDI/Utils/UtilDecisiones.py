from rdflib import Graph

from PracticaECSDI.AgentUtil.ACLMessages import get_message_performative
from PracticaECSDI.Constants import FIPAACLPerformatives
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage
from PracticaECSDI.Utils.UtilAcommodation import askHotelData, processAcommodationResult
from PracticaECSDI.Utils.UtilFlights import askFlightsData, processFlightsResult
from PracticaECSDI.Utils.UtilGeneral import askForInt, askForDate, askForCity

maxPriceFlight = -1
maxPriceHotel = -1
departureCity = ""
arrivalCity = ""
departureDates = ""
returnDates = ""


def askPlanData():
    obtainTravelInfo()

    resultsFlights = askFlightsData(maxPriceFlight, departureDates, returnDates, departureCity, arrivalCity)
    acommodationResults = askHotelData(maxPriceHotel, departureDates, returnDates, arrivalCity)

    graphFlights = Graph().parse(data=resultsFlights.text, format='xml')
    graphAcommodation = Graph().parse(data=acommodationResults.text, format='xml')
    if get_message_performative(graphFlights) == FIPAACLPerformatives.AGREE and get_message_performative(graphAcommodation) == FIPAACLPerformatives.AGREE:
        processFlightsResult(resultsFlights)
        processAcommodationResult(acommodationResults)
    else:
        if get_message_performative(graphFlights) == FIPAACLPerformatives.DISCONFIRM:
            print 'Albaaaaaa'
        if get_message_performative(graphAcommodation) == FIPAACLPerformatives.FAILURE:
            print 'Rafaaaaaa'
    return

def obtainTravelInfo():
    print 'Tell me about your travel'
    global maxPriceFlight
    maxPriceFlight = askForInt("Max price flight: ")

    global maxPriceHotel
    maxPriceHotel = askForInt("Max price hotel: ")

    global departureDates
    departureDates = askForDate("Enter the first day of the travel")

    global returnDates
    returnDates = askForDate("Enter the last day of the travel")

    global departureCity
    departureCity = askForCity("Enter the departure airport (Barcelona, Paris, Londres, Madrid, Estocolmo, Milan): ")

    global arrivalCity
    arrivalCity = askForCity("Enter the arrival airport (Barcelona, Paris, Londres, Madrid, Estocolmo, Milan): ")

