import random

import requests
from rdflib import Graph

from PracticaECSDI.AgentUtil.ACLMessages import build_message, get_message_performative
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Constants.SharedIP import disIP
from PracticaECSDI.Messages.AcommodationRequestMessage import AcommodationRequestMessage
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage


def askHotelData(maxPrice, initDate, finDate, travelCity):
    messageData = AcommodationRequestMessage(random.randint(1, 2000), initDate, finDate, maxPrice, travelCity)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_ACCOMMODATION_REQUEST).serialize(
        format='xml')

    acommURL = disIP.acommodation_IP + str(Constants.PORT_AAcommodation) + "/comm"
    resp = requests.post(acommURL, data=dataContent)

    return resp

def processAcommodationResult(response):
    graph = Graph().parse(data=response.text, format='xml')
    acommResult = AcommodationResponseMessage.from_graph(graph)
    print "---------HOTEL---------"
    print "El hotel encontrado es: "
    print "Nombre: ",acommResult.name
    print "Direccion: ",acommResult.street
    print "Precio: EUR",acommResult.price
    print ""
    return acommResult