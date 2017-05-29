from datetime import date
from rdflib import Graph
from flask import Flask, request, Response
import requests
from PracticaECSDI.Utils.UtilGeneral import askForInt, askForString, askForDate, askForCity
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.FlightRequestMessage import FlightRequestMessage
from PracticaECSDI.Messages.FlightResponseMessage import FlightResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message,get_message_performative
from PracticaECSDI.AgentUtil import ACLMessages

def askFlightsData(maxPrice, initDate, finalDate, departureAirport, arrivalAirport):
    """print 'Tell me about your flights'
    maxPrice = askForInt("Max price: ")
    print 'Max price to request: ', maxPrice
    
    initDate = askForDate("Enter the first day of the travel")
    finalDate = askForDate("Enter the last day of the travel")
    departureAirport = askForCity("Enter the departure airport (Barcelona, Paris, Londres, Madrid, Estocolmo, Milan): ")
    print "Ciudad introducida ", departureAirport
    arrivalAirport = askForCity("Enter the arrival airport (Barcelona, Paris, Londres, Madrid, Estocolmo, Milan): ")"""

    flights_url = Constants.LocalhostUrl + str(Constants.PORT_AFlights) + "/comm"
    print 'url: ', flights_url

    messageDataGo = FlightRequestMessage(1, maxPrice, initDate, finalDate, departureAirport, arrivalAirport)
    gra = messageDataGo.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_FLIGHT_REQUEST).serialize(
        format='xml')

    resp = requests.post(flights_url, data=dataContent)

    #print 'he tornat a la consola clientUI, anem a processar la resposta'
    #processFlightsResult(resp)
    #print "He acabat de processar la resposta"

    return resp

def processFlightsResult(resp):
    flightgo = resp.text
    #print "Register response was {}".format(dat)
    rPerformative1 = get_message_performative(Graph().parse(data=flightgo))
    if rPerformative1 == FIPAACLPerformatives.AGREE:
    #TO-ASK: cal agafar la ontologia de la resposta?
        print "Success request"
        graph = Graph().parse(data=flightgo, format='xml')
        fliResult = FlightResponseMessage.from_graph(graph)

        print "flights: ", fliResult.uuid
        print "price: ", fliResult.price
        print "ID Flight 1: ", fliResult.idflightgo
        print "company 1: ", fliResult.companygo
        print "departure hour 1: ", fliResult.departurehourgo
        print "arrival hour 1: ", fliResult.arrivalhourgo
        print "ID Flight 2: ", fliResult.idflightback
        print "company 2: ", fliResult.companyback
        print "departure hour 2: ", fliResult.departurehourback
        print "arrival hour 2: ", fliResult.arrivalhourback

    else:
        print "There are no flights with those features"
