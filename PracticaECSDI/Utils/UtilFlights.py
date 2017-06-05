import random
from datetime import date
from rdflib import Graph
from flask import Flask, request, Response
import requests

from PracticaECSDI.Constants.SharedIP import disIP
from PracticaECSDI.Utils.UtilGeneral import askForInt, askForString, askForDate, askForCity
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.FlightRequestMessage import FlightRequestMessage
from PracticaECSDI.Messages.FlightResponseMessage import FlightResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message,get_message_performative
from PracticaECSDI.AgentUtil import ACLMessages

def askFlightsData(maxPrice, initDate, finalDate, departureAirport, arrivalAirport):


    flights_url = disIP.flights_IP + str(Constants.PORT_AFlights) + "/comm"

    messageDataGo = FlightRequestMessage(random.randint(1, 2000), maxPrice, initDate, finalDate, departureAirport, arrivalAirport)
    gra = messageDataGo.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_FLIGHT_REQUEST).serialize(
        format='xml')

    resp = requests.post(flights_url, data=dataContent)

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

