from flask import Flask, request, Response
from skyscanner.skyscanner import Flights
from rdflib import Graph
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants

app = Flask(__name__)
service = None


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'Im in Flights Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.FLIGHT_REQUEST:
        print 'Its a flight request'
        flights = getFlies(graph)
        return flights.serialize()
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)



def getFlights(graph):
    print 'im in get flies from graph'
    return "FLights response"

def getFlies(maxprice, initDate, finalDate, fromCity, toCity):
    # GO TO SKYSCANER and get the vuelos anda i tornada
    # api-key: fi768769083827246592561385220425 (conta de cris)
    # https://skyscanner.github.io/slate/#browse-quotes
    # outboundPartialDate: (required) Format "yyyy-mm-dd", "yyyy-mm" or "anytime".
    # inboundPartialDate: (optional) Format "yyyy-mm-dd", "yyyy-mm" or "anytime". Use empty string for oneway trip.
    # examples: https://skyscanner.readthedocs.io/en/latest/usage.html

    flights_service = Flights('fi768769083827246592561385220425')

    if fromCity =='Barcelona':
        fromCity='BCN'
        count='ES'
    elif fromCity == 'Paris':
        fromCity = 'PARI'
        count = 'FR'
    elif fromCity == 'Londres':
        fromCity = 'LOND'
        count='UK'
    elif fromCity == 'Madrid':
        fromCity = 'MAD'
        count='ES'
    elif fromCity == 'Estocolm':
        fromCity = 'STOC'
        count='SE'
    elif fromCity == 'Milan':
        fromCity = 'Mila'
        count='IT'

    """ result = flights_service.get_result(
    country=count,
    currency='EUR',
    locale='es-ES',
    originplace=fromCity,
    destinationplace=toCity,
    outbounddate=initDate,
    inbounddate=finalDate,
    adults=1).parsed"""

    result = flights_service.get_result(
    country='UK',
    currency='GBP',
    locale='en-GB',
    originplace='SIN-sky',
    destinationplace='KUL-sky',
    outbounddate='2017-05-28',
    inbounddate='2017-05-31',
    adults=1).parsed

    return result

if __name__ == '__main__':
    app.run(port=Constants.PORT_AFlights, debug=True)
