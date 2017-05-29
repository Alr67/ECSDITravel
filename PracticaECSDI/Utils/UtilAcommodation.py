import requests
from rdflib import Graph

from PracticaECSDI.AgentUtil.ACLMessages import build_message, get_message_performative
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.AcommodationRequestMessage import AcommodationRequestMessage
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage
from PracticaECSDI.Utils.UtilGeneral import askForInt, askForDate, askForCity


def askHotelData(maxPrice, initDate, finDate, travelCity):
    """ print 'Tell me about your hotels'
    maxPrice = askForInt("Max price: ")
    print 'Max price to request: ', maxPrice
    
    initDate = askForDate("Enter the check in date")
    finDate = askForDate("Enter check out date")
    travelCity = askForCity("Enter the city where you will stay (Barcelona, Paris, Londres, Madrid, Estocolmo, Milan): ")"""
    messageData = AcommodationRequestMessage(1, initDate, finDate, maxPrice, travelCity)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_ACOMMODATION_REQUEST).serialize(
        format='xml')


    acommURL = Constants.LocalhostUrl + str(Constants.PORT_AAcommodation) + "/comm"
    print 'url: ', acommURL
    resp = requests.post(acommURL, data=dataContent)
    #print 'he tornat a la consola clientUI, anem a processar la resposta'
    #processAcommodationResult(resp)
    #print "He acabat de processar la resposta"

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