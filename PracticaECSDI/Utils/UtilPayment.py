import random

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
                a = 1
                return
    except ValueError:
        print "Error a la hora de gestionar el pago"


def askPaymentData(vuelos, hotel):
    print 'Introduce a continuacion la informacion para realizar el pago:'
    print '\nNombre del titular de la tarjeta:'
    name = raw_input("")
    print '\nNumero de tarjeta:'
    card_num = raw_input("")
    print '\nProcesando el pago...'
    payURL = disIP.payment_IP + str(Constants.PORT_APayment) + "/comm"
    hotelPrice = hotel.price
    flightPrice = vuelos.price
    try:
        defFlightPrice = flightPrice.replace("EUR", '')
        amountHotel =float(hotelPrice)
        amountFlight = float(defFlightPrice)
        amount = amountHotel + amountFlight
    except ValueError:
        print "No se ha podido hacer el parse a float"
        return
    messageData = PaymentRequestMessage(random.randint(1, 2000), name, card_num, amount)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_PAYMENT_REQUEST)\
        .serialize(format='xml')
    resp = requests.post(payURL, data=dataContent)
    processPaymentResult(resp, vuelos, hotel)
    return


def processPaymentResult(response, flights, accomm):
    graph = Graph().parse(data=response.text, format='xml')
    if get_message_performative(graph) == FIPAACLPerformatives.AGREE:
        paymentResult = PaymentResponseMessage.from_graph(graph)
        print '\nPago realizado correctamente'
        print '\nProcesando factura...\n\n'
        print '---------Factura---------'
        print flights.companygo, " ", flights.idflightgo, " + ", flights.companyback, " ", flights.idflightback,\
            " -> ", flights.price
        print accomm.name, " -> ", accomm.price
        print "\nCantidad total: ", paymentResult.amount, "EUR"
        print '\n\nGracias por usar nuestro servicio!\n'
    elif get_message_performative(graph) == FIPAACLPerformatives.FAILURE:
        print "No se ha podido contactar con los proveedores para realizar el pago."



