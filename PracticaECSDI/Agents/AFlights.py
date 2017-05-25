from flask import Flask, request, Response
from skyscanner.skyscanner import Flights
from rdflib import Graph
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from PracticaECSDI.Messages.FlightRequestMessage import FlightRequestMessage
from PracticaECSDI.Messages.FlightResponseMessage import FlightResponseMessage
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants

import json
import urllib2
import requests

QPX_END_POINT = 'https://www.googleapis.com/qpxExpress/v1/trips/search'
QPX_API_KEY = 'AIzaSyBmqGFeBCyqLUUvhvbS8WPOnm5WxVX2Vrk'
headers = {'content-type': 'application/json'}

app = Flask(__name__)
service = None


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_FLIGHT_REQUEST:
        flights = getFlights(graph)
        return flights
    else:
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)

@app.route('/itstime', methods=['GET', 'POST', 'PUT'])
def time_to_send():
    return service.time_to_send()

def getFlights(graph):
    print 'im in get flights from graph'

    data = FlightRequestMessage.from_graph(graph)

    print 'data obtained: ', data
    print 'initDate: ', data.firstDay
    print 'lastDay: ', data.lastDay
    print 'maxPrice: ', data.maxPrice
    print 'departureAirport: ', data.departureAirport
    print 'arrivalAirport: ', data.arrivalAirport

    print "EUR" + str(data.maxPrice)

    #Request google flights

    code = {
        "request": {
            "slice": [
                {
                    "origin": data.departureAirport,
                    "destination": data.arrivalAirport,
                    "date": data.firstDay.strftime("%Y-%m-%d")
                },
                {
                    "origin": data.arrivalAirport,
                    "destination": data.departureAirport,
                    "date": data.lastDay.strftime("%Y-%m-%d")
                }
            ],
            "passengers": {
                "adultCount": 1,
                "infantInLapCount": 0,
                "infantInSeatCount": 0,
                "childCount": 0,
                "seniorCount": 0
            },
            "solutions": 1,
            "maxPrice": "EUR" + str(data.maxPrice),
            "saleCountry": "ES",
            "refundable": "false"
        }
    }

    r = requests.post(QPX_END_POINT, params={'key': QPX_API_KEY}, data=json.dumps(code), headers=headers)
    result = r.json()

    if 'tripOption' in result['trips']:
        for trip in result['trips']['tripOption']:
            price = trip['pricing'][0]['saleTotal']

            idflightgo = trip['slice'][0]['segment'][0]['flight']['number']
            companygo = trip['slice'][0]['segment'][0]['flight']['carrier']
            departurehourgo = trip['slice'][0]['segment'][0]['leg'][0]['departureTime']
            arrivalhourgo = trip['slice'][0]['segment'][0]['leg'][0]['arrivalTime']

            idflightreturn = trip['slice'][1]['segment'][0]['flight']['number']
            companyreturn = trip['slice'][1]['segment'][0]['flight']['carrier']
            departurehourreturn = trip['slice'][1]['segment'][0]['leg'][0]['departureTime']
            arrivalhourreturn = trip['slice'][1]['segment'][0]['leg'][0]['arrivalTime']


        responseObj = FlightResponseMessage(data.uuid, price, idflightgo, companygo, departurehourgo, arrivalhourgo,
                                            idflightreturn, companyreturn, departurehourreturn, arrivalhourreturn)
        dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE,
                                    Ontologies.SEND_ACTIVITIES_RESPONSE).serialize(format='xml')
        return dataContent

    else:
        responseObj = FlightResponseMessage(0, 0, 0, 0, 0, 0)
        dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.DISCONFIRM,
                                    Ontologies.SEND_ACTIVITIES_RESPONSE).serialize(format='xml')
        return dataContent

if __name__ == '__main__':
    app.run(port=Constants.PORT_AFlights, debug=True)
