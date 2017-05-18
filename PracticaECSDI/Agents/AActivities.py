from flask import Flask, request, Response
from rdflib import Graph
from AgentUtil import  ACLMessages
from Constants import  Ontologies, FIPAACLPerformatives, Constants
from Messages.ActivitiesRequestMessage import ActivitiesRequestMessage


app = Flask(__name__)
service = None

@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'Im in Activities Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.ACTIVITIES_REQUEST:
        print 'Its a activity request'
        act = getActivities(graph)
        return act.serialize()
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
    return "Activities response"

    return result

if __name__ == '__main__':
    app.run(port=Constants.PORT_AActivities, debug=True)
