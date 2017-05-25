import requests
from rdflib import Graph

from PracticaECSDI.AgentUtil.ACLMessages import build_message, get_message_performative
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages import AcommodationResponseMessage
from PracticaECSDI.Messages.AcommodationRequestMessage import AcommodationRequestMessage
from PracticaECSDI.Utils.UtilGeneral import askForString, askForInt, askForDate


def askHotelData():
    print 'Tell me about your hotels'
    maxPrice = askForInt("Max price: ")
    print 'Max price to request: ', maxPrice
    acommURL = Constants.LocalhostUrl + str(Constants.PORT_AAcommodation) + "/comm"
    print 'url: ', acommURL
    initDate = askForDate("Enter the check in date")
    finDate = askForDate("Enter check out date")
    travelCity = askForString("Tell me where")
    messageData = AcommodationRequestMessage(1, initDate, finDate, maxPrice, travelCity)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.SEND_ACOMMODATION_REQUEST).serialize(
        format='xml')

    resp = requests.post(acommURL, data=dataContent)
    print 'he tornat a la consola clientUI, anem a processar la resposta'
    processAcommodationResult(resp)
    print "He acabat de processar la resposta"

    return

def processAcommodationResult(response):
    #print "Register response was {}".format(dat)
    #rPerformative = get_message_performative(Graph().parse(data=dat))
    #if rPerformative == FIPAACLPerformatives.AGREE:
    #TO-ASK: cal agafar la ontologia de la resposta?

    graph = Graph().parse(data=response.text, format='xml')
    if get_message_performative(graph) == FIPAACLPerformatives.AGREE:
        print "Success request"
        acommResult = AcommodationResponseMessage.from_graph(graph)
        print acommResult

    #else:
        #print "Activities error"