import requests
from flask import Flask, request, Response
from rdflib import Graph
import datetime
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.AcommodationRequestMessage import AcommodationRequestMessage
from PracticaECSDI.Messages.AcommodationResponseMessage import AcommodationResponseMessage
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from PracticaECSDI.Utils.UtilGeneral import askForCityLat, askForCityLong

app = Flask(__name__)
service = None

@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'I am in Acommodation Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_ACOMMODATION_REQUEST:
        print 'Its an acommodation request'
        message = getAcommodation(graph)
        print 'activities graph obtained, lets construct response message'
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)


def getAcommodation(graph):
    print 'im getting your hotel preferences from graph'
    data = AcommodationRequestMessage.from_graph(graph)
    print 'data obtained: ',data
    print  'initDate: ',data.firstDay
    print  'lastDay: ',data.lastDay
    print  'maxPrice: ',data.maxPrice
    print 'la ciudad es: ', data.city
    contactWithHotelProvider(data.firstDay,data.lastDay, data.city)
    responseObj = AcommodationResponseMessage(1,"Ritz", 40, "Liverpool Street 15, SS0 0B7, City of London")
    #TO-ASK: Cal ontologia de resposta tambe??? O amb performativa ja n'hi ha prou?
    dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE, Ontologies.SEND_ACOMMODATION_RESPONSE).serialize(format='xml')
    return dataContent


def contactWithHotelProvider(check_in, check_out, city):
    print 'lets connect with the hotels API'
    lat = askForCityLat(city)
    long = askForCityLong(city)
    print ' We are about to ask the API. The lat is', lat
    urlRequest = 'http://api.sandbox.amadeus.com/v1.2/hotels/search-circle?apikey=9eaVp6HVlEMrIFFyY5gbUFC1FAD6c1iT&latitude={reqLat}&longitude={reqLon}&radius=20&check_in={reqArr}&check_out={reqDep}&currency=EUR&number_of_results=1'.format(reqLat=lat, reqLon=long, reqArr=check_in, reqDep=check_out)
    print 'La solicitud se hace a ', urlRequest
    answer = requests.request('GET', urlRequest)
    print answer.content


if __name__ == '__main__':
    app.run(port=Constants.PORT_AAcommodation, debug=True)