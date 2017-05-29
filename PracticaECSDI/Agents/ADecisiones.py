import requests
from flask import Flask, request, json
from rdflib import Graph
import datetime
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.AcommodationRequestMessage import AcommodationRequestMessage
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from PracticaECSDI.Utils.UtilGeneral import askForCityLat, askForCityLong

app = Flask(__name__)
service = None

@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'I am in Decisiones Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_PLAN_REQUEST:
        print 'Its an plan request'
        message = getPlan(graph)
        print 'Plan graph obtained, lets construct response message'
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)

def getPlan(graph):

    return

if __name__ == '__main__':
    app.run(port=Constants.PORT_ADecisiones, debug=True)