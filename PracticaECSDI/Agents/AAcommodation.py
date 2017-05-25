from flask import Flask, request, Response
from rdflib import Graph
import datetime
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.AcommodationRequestMessage import AcommodationRequestMessage
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage, DayPlan
from PracticaECSDI.AgentUtil.ACLMessages import build_message

app = Flask(__name__)
service = None

@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'Im in Acommodation Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_ACOMMODATION_REQUEST:
        print 'Its an acommodation request'
        message = getActivities(graph)
        print 'activities graph obtained, lets construct response message'
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)


def getActivities(graph):
    print 'im in get activities from graph'
    data = AcommodationRequestMessage.from_graph(graph)
    print 'data obtained: ',data
    print  'initDate: ',data.firstDay
    print  'lastDay: ',data.lastDay
    print  'maxPrice: ',data.maxPrice
    days = (data.lastDay-data.firstDay).days
    print 'days: ',days
    planList = []
    for i in range(days):
        dayPlan = DayPlan(i,data.firstDay+ datetime.timedelta(days=i),"Pending","Pending","Pending")
        planList.append(dayPlan)
    print 'plan length: ',len(planList)
    responseObj = AcommodationResponseMessage(1,planList)
    #TO-ASK: Cal ontologia de resposta tambe??? O amb performativa ja n'hi ha prou?
    dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE, Ontologies.SEND_ACTIVITIES_RESPONSE).serialize(format='xml')
    return dataContent


if __name__ == '__main__':
    app.run(port=Constants.PORT_AAcommodation, debug=True)