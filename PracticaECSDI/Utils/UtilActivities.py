from datetime import date
from rdflib import Graph
from flask import Flask, request, Response
import requests
from PracticaECSDI.Utils.UtilGeneral import askForInt,askForString,askForDate
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.ActivitiesRequestMessage import ActivitiesRequestMessage
from PracticaECSDI.Messages.ActivitiesResponseMessage import ActivitiesResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message,get_message_performative
from PracticaECSDI.Utils.UtilGeneral import askForCity, askForTravelType,CodeToCityLocation
from PracticaECSDI.AgentUtil import ACLMessages

def directToAct(location,type):
    city = CodeToCityLocation(location)
    activities_url = Constants.LocalhostUrl + str(Constants.PORT_AActivities) + "/comm"
    messageData = ActivitiesRequestMessage(1, date(2017,7,1),date(2017,7,3),200,city,type)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_ACTIVITIES_REQUEST).serialize(format='xml')
    resp = requests.post(activities_url, data=dataContent)
    processActivitiesResult(resp)
    print "Gracies per confiar en nosaltres, disfruti del plan :)"
    return

def askActivitiesData():
    print 'Im in askActivitiesData'
    arrivalCity = askForCity("Enter the arrival airport (Barcelona, Paris, Londres, Madrid, Estocolmo, Milan): ")
    type = askForTravelType()
    directToAct(arrivalCity,type)

    return
def askForActivities(firstDay,lastDay,location,type):
    city = CodeToCityLocation(location)
    activities_url = Constants.LocalhostUrl + str(Constants.PORT_AActivities) + "/comm"
    messageData = ActivitiesRequestMessage(1,firstDay,lastDay,200,city,type)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_ACTIVITIES_REQUEST).serialize(format='xml')
    resp = requests.post(activities_url, data=dataContent)
    return resp

def processActivitiesResult(response):
    graph = Graph().parse(data=response.text, format='xml')
    actResult = ActivitiesResponseMessage.from_graph(graph)
    print "---------Activities---------"
    for day in actResult.day_plans:
        print "--Dia: ", day.uuid
        print "     Data: ", day.date
        print "     Actividad manana: ", day.activity1
        print "     Actividad mediodia: ", day.activity2
        print "     Actividad tarde: ", day.activity3
        print ""