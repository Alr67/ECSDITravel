from datetime import date
from rdflib import Graph
from flask import Flask, request, Response
import requests
from PracticaECSDI.Utils.UtilGeneral import askForInt,askForString,askForDate
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.FlightRequestMessage import FlightRequestMessage
from PracticaECSDI.Messages.FlightResponseMessage import FlightResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message,get_message_performative
from PracticaECSDI.AgentUtil import ACLMessages

def askFlightsData():
    print 'Tell me about your flights'
    maxPrice = askForInt("Max price: ")
    print 'Max price to request: ', maxPrice
    flights_url = Constants.LocalhostUrl + str(Constants.PORT_AFlights) + "/comm"
    print 'url: ', flights_url
    initDate = askForDate("Enter the first day of the travel")
    finDate = askForDate("Enter the last day of the travel")
    departureAirport = askForString("Enter the departure airport (Barcelona, Paris, Londres):")
    arrivalAirport = askForString("Enter the arrival airport (Barcelona, Paris, Londres):")
    #departureAirport = cityConversor(departureAirport)
    #arrivalAirport = cityConversor(arrivalAirport)

    #Vuelo ida
    messageDataGo = FlightRequestMessage(1, maxPrice,initDate, finDate, departureAirport, arrivalAirport)
    gra = messageDataGo.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_FLIGHT_REQUEST).serialize(
        format='xml')

    resp1 = requests.post(flights_url, data=dataContent)

    #Vuelo vuelta
    priceRestante = getPriceFlight(resp1)
    messageDataReturn = FlightRequestMessage(1, priceRestante,initDate, finDate, arrivalAirport, departureAirport)
    gra = messageDataReturn.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_FLIGHT_REQUEST).serialize(
        format='xml')

    resp2 = requests.post(flights_url, data=dataContent)


    print 'he tornat a la consola clientUI, anem a processar la resposta'
    processFlightsResult(resp1, resp2)
    print "He acabat de processar la resposta"

    return

def getPriceFlight(resp1):
    flightgo = resp1.text
    # print "Register response was {}".format(dat)
    rPerformative1 = get_message_performative(Graph().parse(data=flightgo))
    if rPerformative1 == FIPAACLPerformatives.AGREE:
        graph = Graph().parse(data=flightgo, format='xml')
        fliResult = FlightResponseMessage.from_graph(graph)
        return fliResult.price
    return

def processFlightsResult(resp1, resp2):
    flightgo = resp1.text
    #print "Register response was {}".format(dat)
    rPerformative1 = get_message_performative(Graph().parse(data=flightgo))
    if rPerformative1 == FIPAACLPerformatives.AGREE:
    #TO-ASK: cal agafar la ontologia de la resposta?
        print "Success request"
        graph = Graph().parse(data=flightgo, format='xml')
        fliResult = FlightResponseMessage.from_graph(graph)

        print "flight 1: ", len(fliResult.uuid)
        print "ID Flight 1: ", len(fliResult.idflight)
        print "price 1: ", len(fliResult.price)
        print "company 1: ", len(fliResult.company)
        print "departure hour 1: ", len(fliResult.departurehour)
        print "arrival hour 1: ", len(fliResult.arrival)
    else:
        print "Flight 1 error"

    flightreturn = resp2.text
    # print "Register response was {}".format(dat)
    rPerformative2 = get_message_performative(Graph().parse(data=flightreturn))
    if rPerformative2 == FIPAACLPerformatives.AGREE:
        print "Success request"
        graph = Graph().parse(data=flightreturn, format='xml')
        fliResult = FlightResponseMessage.from_graph(graph)

        print "flight 2: ", len(fliResult.uuid)
        print "ID Flight 2: ", len(fliResult.idflight)
        print "price 2: ", len(fliResult.price)
        print "company 2: ", len(fliResult.company)
        print "departure hour 2: ", len(fliResult.departurehour)
        print "arrival hour 2: ", len(fliResult.arrival)
    else:
        print "Flight 2 error"

def cityConversor(city):
    if city == 'Barcelona':
        resCity = 'BCN'
        #count = 'ES'
    elif city == 'Paris':
        resCity = 'PARI'
        #count = 'FR'
    elif city == 'Londres':
        resCity = 'LOND'
        #count = 'UK'
    """ elif city == 'Madrid':
        resCity = 'MAD'
        #count = 'ES'
    elif city == 'Estocolm':
        resCity = 'STOC'
        #count = 'SE'
    elif city == 'Milan':
        resCity = 'Mila'
        #count = 'IT'"""

    return resCity