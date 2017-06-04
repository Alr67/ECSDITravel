from flask import Flask, request, Response
from rdflib import Graph
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.PaymentRequestMessage import PaymentRequestMessage
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
        print 'Creo que funciona hasta aqui............'

        message = processPaymentRequest(graph)
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(),
            FIPAACLPerformatives.NOT_UNDERSTOOD,
            Ontologies.UNKNOWN_ONTOLOGY)

def processPaymentRequest(graph):
    print 'processPaymentRequest'
    resp = PaymentRequestMessage.from_graph(graph)
    print 'after from graph, obj obtained: ',resp
    proc =  processPaymentResponse(resp)
    return proc

def processPaymentResponse(resp):
    print 'processPaymentResponse with, ',resp
    response = PaymentResponseMessage(resp.name, resp.card, resp.amount)
    print 'after create response'
    dataContent = build_message(response.to_graph(), FIPAACLPerformatives.AGREE,
                                Ontologies.SEND_PAYMENT_RESPONSE).serialize(format='xml')
    print 'after building Message'
    return dataContent

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=Constants.PORT_APayment, debug=True)
