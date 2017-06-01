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
    graph = Graph().parse(data=flightgo, format='xml')
    fliResult = FlightResponseMessage.from_graph(graph)

    print "---------VUELOS----------"
    print "Informacion sobre los vuelos encontrados:"
    print ' '
    print "Precio vuelos: ", fliResult.price
    print ' '
    print "ID Vuelo ida: ", fliResult.idflightgo
    print "Companyia vuelo ida: ", fliResult.companygo
    print "Hora de salida vuelo ida: ", fliResult.departurehourgo
    print "Hora de llegada vuelo ida: ", fliResult.arrivalhourgo
    print ' '
    print "ID Vuelo vuelta: ", fliResult.idflightback
    print "Companyia vuelo vuelta: ", fliResult.companyback
    print "Hora de salida vuelo vuelta: ", fliResult.departurehourback
    print "Hora de llegada vuelo vuelta: ", fliResult.arrivalhourback
    print ""
    return fliResult

