from flask import Flask, request, Response
from rdflib import Graph
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages import PaymentRequestMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from PracticaECSDI.Messages.PaymentResponseMessage import PaymentResponseMessage

google_places = ""
app = Flask(__name__)
service = None


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_PAYMENT_REQUEST:
        message = processPaymentRequest(graph)
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(),
            FIPAACLPerformatives.NOT_UNDERSTOOD,
            Ontologies.UNKNOWN_ONTOLOGY)

def processPaymentRequest(graph):
    #do payment stuff
    resp = PaymentRequestMessage.from_graph(graph)
    return processPaymentResponse(resp)

def processPaymentResponse(resp):
    response = PaymentResponseMessage(resp.name, resp.card, resp.amount)
    dataContent = build_message(response.to_graph(), FIPAACLPerformatives.AGREE,
                                Ontologies.SEND_PAYMENT_RESPONSE).serialize(format='xml')
    return dataContent

if __name__ == '__main__':
    app.run(host='192.168.0.161',port=Constants.PORT_APayment, debug=True)