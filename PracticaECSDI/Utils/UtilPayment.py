import requests
from rdflib import Graph
from PracticaECSDI.AgentUtil.ACLMessages import build_message, get_message_performative
from PracticaECSDI.Constants import Constants, FIPAACLPerformatives, Ontologies
from PracticaECSDI.Constants.SharedIP import disIP
from PracticaECSDI.Messages.PaymentResponseMessage import PaymentResponseMessage
from PracticaECSDI.Messages.PaymentRequestMessage import PaymentRequestMessage
from PracticaECSDI.Utils.UtilGeneral import askForString


def askPayment(vuelos, hotel):
    print "\nQuieres confirmar y pagar este viaje?"
    print "1. Si"
    print "2. No"
    try:
        option = raw_input("")
        option = int(option)
        if option not in [1, 2]:
            print ("Opcion incorrecta")
        else:
            if option == 1:
                askPaymentData(vuelos, hotel)
                return
            if option == 2:
                a = 1  # something
                return
    except ValueError:
        print "Este valor debe ser numerico"


def askPaymentData(vuelos, hotel):
    print 'Introduce a continuacion la informacion para realizar el pago:'
    print '\nNombre del titular de la tarjeta:'
    name = askForString("")
    print name;
    name = 'Bubu'
    print '\nNumero de tarjeta:'
    cardNum = askForString("")
    cardNum = '123'
    print '\nProcesando el pago...'
    payURL = disIP.payment_IP + str(Constants.PORT_APayment) + "/comm"
    print 'url: ', payURL
    amount = vuelos.price, ' + ', hotel.price
    #messageData = PaymentRequestMessage(name, cardNum, amount)
    messageData = PaymentRequestMessage(1,'gulle', '123', '234')
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_PAYMENT_REQUEST)\
        .serialize(format='xml')
    resp = requests.post(payURL, data=dataContent)
    processPaymentResult(resp, vuelos, hotel)
    return


def processPaymentResult(response, flights, accomm):
    graph = Graph().parse(data=response.text, format='xml')
    if get_message_performative(graph) == FIPAACLPerformatives.AGREE:
        print '\nIm back'
        paymentResult = PaymentResponseMessage.from_graph(graph)
        print '\nPago realizado correctamente'
        print '\nProcesando factura...\n\n'
        print flights.companygo, " ", flights.idflightgo, " + ", flights.companyback, " ", flights.idflightback,\
            " -> ", flights.price
        print accomm.name, " -> ", accomm.price
        print "\n\nCantidad total: ", paymentResult.amount
        print '\n\nGracias por usar nuestro servicio.'
    elif get_message_performative(graph) == FIPAACLPerformatives.FAILURE:
        print "No se ha podido contactar con los proveedores para realizar el pago."

