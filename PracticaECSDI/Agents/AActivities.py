from flask import Flask, request, Response
from rdflib import Graph
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants

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
    return "Activities response"

    return result

if __name__ == '__main__':
    app.run(port=Constants.PORT_AActivities, debug=True)
