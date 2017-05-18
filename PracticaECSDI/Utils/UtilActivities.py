from datetime import date
from rdflib import Graph
from flask import Flask, request, Response
import requests
from PracticaECSDI.Utils.UtilGeneral import askForInt,askForString
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.ActivitiesRequestMessage import ActivitiesRequestMessage
from PracticaECSDI.Messages.ActivitiesResponseMessage import ActivitiesResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message,get_message_performative
from PracticaECSDI.AgentUtil import ACLMessages


def askActivitiesData():
    print 'Tell me about your activities'
    maxPrice = askForInt("Max price: ")
    print 'Max price to request: ', maxPrice
    activities_url = Constants.LocalhostUrl + str(Constants.PORT_AActivities) + "/comm"
    print 'url: ', activities_url
    initDate = date(2011,11,17)
    finDate = date(2011,11,24)
    messageData = ActivitiesRequestMessage(1, initDate,finDate,maxPrice)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_ACTIVITIES_REQUEST).serialize(format='xml')

    resp = requests.post(activities_url, data=dataContent)
    print 'he tornat a la consola clientUI, anem a processar la resposta'
    processActivitiesResult(resp)
    print "He acabat de processar la resposta"

    return

def processActivitiesResult(response):
    dat = response.text
    #print "Register response was {}".format(dat)
    rPerformative = get_message_performative(Graph().parse(data=dat))
    if rPerformative == FIPAACLPerformatives.AGREE:
    #TO-ASK: cal agafar la ontologia de la resposta?
        print "Success request"
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
