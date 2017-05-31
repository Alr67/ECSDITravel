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
    print 'Ja tinc les activitats, processant la resposta...'
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
    print 'Ja tinc les activitats, processant la resposta...'
    processActivitiesResult(resp)
    print "Gracies per confiar en nosaltres, disfruti del plan :)"

def processActivitiesResult(response):
    dat = response.text
    print 'vaig a processar3'
   # print "Register response was {}".format(dat)
    print 'vaig a processar'
    rPerformative = get_message_performative(Graph().parse(data=dat))
    print 'vaig a processar2'
    if rPerformative == FIPAACLPerformatives.AGREE:
    #TO-ASK: cal agafar la ontologia de la resposta?
        print 'Agree'
        graph = Graph().parse(data=dat, format='xml')
        actResult = ActivitiesResponseMessage.from_graph(graph)

        print "dies: ", len(actResult.day_plans)
        for day in actResult.day_plans:
            print "dia ",day.uuid
            print "Data: ",day.date
            print "Activitat1: ",day.activity1
            print "Activitat2: ",day.activity2
            print "Activitat3: ",day.activity3

    else:
        print "Activities error"
