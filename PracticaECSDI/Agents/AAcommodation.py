import random

import requests
from flask import Flask, request, json
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
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_ACCOMMODATION_REQUEST:
        message = getAcommodation(graph)
        return message
    else:
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)


def getAcommodation(graph):
    print 'im getting your hotel preferences from graph'
    data = AcommodationRequestMessage.from_graph(graph)
    responseObj = contactWithHotelProvider(data.firstDay,data.lastDay, data.city, data.maxPrice)
    if responseObj.price > 0:
        dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE, Ontologies.SEND_ACCOMMODATION_RESPONSE).serialize(format='xml')
    else:
        dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.FAILURE, Ontologies.SEND_ACCOMMODATION_RESPONSE).serialize(format='xml')
    return dataContent


def contactWithHotelProvider(check_in, check_out, city, maxPrice):
    print 'lets connect with the hotels API'
    lat = askForCityLat(city)
    long = askForCityLong(city)
    urlRequest = 'http://api.sandbox.amadeus.com/v1.2/hotels/search-circle?apikey=9eaVp6HVlEMrIFFyY5gbUFC1FAD6c1iT&latitude={reqLat}&longitude={reqLon}&radius=20&check_in={reqArr}&check_out={reqDep}&currency=EUR&number_of_results=1'.format(reqLat=lat, reqLon=long, reqArr=check_in, reqDep=check_out)
    print 'La solicitud se hace a ', urlRequest
    answer = requests.request('GET', urlRequest)
    content = answer.json()
    hotelPrice = content['results'][0]['total_price']['amount']
    hotelName = content['results'][0]['property_name']
    calle = content['results'][0]['address']['line1']
    cp = content['results'][0]['address']['postal_code']
    ciudad = content['results'][0]['address']['city']
    direccion = ''.join([calle,', ',ciudad,', ',cp])
    print 'El precio del hotel es ',float(hotelPrice)
    print 'El max es ', maxPrice
    if float(hotelPrice) <= maxPrice:
        finalMessage = AcommodationResponseMessage(random.randint(1, 2000), hotelName, hotelPrice, direccion)
    else:
        finalMessage = AcommodationResponseMessage(random.randint(1, 2000), 'error', -1, 'error')
    return finalMessage



if __name__ == '__main__':
    app.run(host=Constants.IP_AAccommodation, port=Constants.PORT_AAcommodation, debug=True)