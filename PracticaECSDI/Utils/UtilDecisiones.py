from rdflib import Graph

from PracticaECSDI.AgentUtil.ACLMessages import get_message_performative
from PracticaECSDI.Constants import FIPAACLPerformatives
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage
from PracticaECSDI.Utils.UtilAcommodation import askHotelData, processAcommodationResult
from PracticaECSDI.Utils.UtilFlights import askFlightsData, processFlightsResult
from PracticaECSDI.Utils.UtilActivities import askForActivities,processActivitiesResult
from PracticaECSDI.Utils.UtilGeneral import askForInt, askForDate, askForCity,askForTravelType

maxPriceFlight = -1
maxPriceHotel = -1
departureCity = ""
arrivalCity = ""
departureDates = ""
returnDates = ""
travelType=""


def askPlanData():
    obtainTravelInfo()

    resultsFlights = askFlightsData(maxPriceFlight, departureDates, returnDates, departureCity, arrivalCity)
    acommodationResults = askHotelData(maxPriceHotel, departureDates, returnDates, arrivalCity)
    activitiesResults = askForActivities(departureDates,returnDates,arrivalCity,travelType)

    graphFlights = Graph().parse(data=resultsFlights.text, format='xml')
    graphAcommodation = Graph().parse(data=acommodationResults.text, format='xml')
    graphActivities = Graph().parse(data=activitiesResults.text,format='xml')

    if get_message_performative(graphFlights) == FIPAACLPerformatives.AGREE and get_message_performative(graphAcommodation) == FIPAACLPerformatives.AGREE and get_message_performative(graphActivities) == FIPAACLPerformatives.AGREE:
    #if get_message_performative(graphFlights) == FIPAACLPerformatives.AGREE  and get_message_performative(graphActivities)==FIPAACLPerformatives.AGREE:
        processFlightsResult(resultsFlights)
        processAcommodationResult(acommodationResults)
        processActivitiesResult(activitiesResults)
    else:
        print 'El viaje no se ha podido planear. El motivo ha sido: '
        if get_message_performative(graphFlights) == FIPAACLPerformatives.DISCONFIRM:
            print 'No se han encontrado vuelos para las fechas y precio seleccionados'
        if get_message_performative(graphAcommodation) == FIPAACLPerformatives.FAILURE:
            print 'No se ha encontrado ningun hotel para las fechas y precio seleccionado'
        if get_message_performative(graphActivities) == FIPAACLPerformatives.FAILURE:
            print 'No se ha encontrado ninguna actividad para la ciudad y tipo de viaje'
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

    global travelType
    travelType = askForTravelType()

def processPlanRequest(initDate,endDate,maxPriceHotel,maxPriceFlight,arrivalCity,departureCity,travelType):
    #per la documentacio
    return