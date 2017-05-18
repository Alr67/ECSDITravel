from flask import Flask, request, Response
from rdflib import Graph
import datetime
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.ActivitiesRequestMessage import ActivitiesRequestMessage
from PracticaECSDI.Messages.ActivitiesResponseMessage import ActivitiesResponseMessage,DayPlan
from PracticaECSDI.AgentUtil.ACLMessages import build_message

app = Flask(__name__)
service = None

@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'Im in Activities Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_ACTIVITIES_REQUEST:
        print 'Its a activity request'
        message = getActivities(graph)
        print 'activities graph obtained, lets construct response message'
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)


def getActivities(graph):
    print 'im in get activities from graph'
    data = ActivitiesRequestMessage.from_graph(graph)
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
    responseObj = ActivitiesResponseMessage(1,planList)
    #TO-ASK: Cal ontologia de resposta tambe??? O amb performativa ja n'hi ha prou?
    dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE, Ontologies.SEND_ACTIVITIES_RESPONSE).serialize(format='xml')
    return dataContent


if __name__ == '__main__':
    app.run(port=Constants.PORT_AActivities, debug=True)
