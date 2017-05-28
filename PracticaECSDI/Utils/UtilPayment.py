from rdflib import Graph
from PracticaECSDI.AgentUtil.ACLMessages import build_message, get_message_performative
from PracticaECSDI.Constants import Constants, FIPAACLPerformatives, Ontologies
from PracticaECSDI.Messages import PaymentResponseMessage
from PracticaECSDI.Messages.PaymentRequestMessage import PaymentRequestMessage
import requests

from PracticaECSDI.Utils.UtilGeneral import askForString


def askPaymentData():
    print 'Introduce a continuacion la informacion para realizar el pago:'
    print '\nNombre del titular de la tarjeta:'
    name = askForString("")
    print '\nNumero de tarjeta:'
    cardNum = askForString("")
    print '\nProcesando el pago...'
    payURL = Constants.LocalhostUrl + str(Constants.PORT_APayment) + "/comm"
    print 'url: ', payURL
    amount = '546 Euros'
    messageData = PaymentRequestMessage(name, cardNum, amount)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_PAYMENT_REQUEST)\
        .serialize(format='xml')

    resp = requests.post(payURL, data=dataContent)
    print '\nPago realizado correctamente'
    print '\nProcesando factura...'
    processPaymentResult(resp)
    return

def processPaymentResult(response):
    graph = Graph().parse(data=response.text, format='xml')
    if get_message_performative(graph) == FIPAACLPerformatives.AGREE:
        paymentResult = PaymentResponseMessage.from_graph(graph)
        print "Se ha pagado correctamente la cantidad de ", paymentResult.amount, ' relativa a los vuelos y alojamientos'
        print '\n\nGracias por usar nuestro servicio.'
    elif get_message_performative(graph) == FIPAACLPerformatives.FAILURE:
        print "No se ha podido contactar con los proveedores para realizar el pago."

