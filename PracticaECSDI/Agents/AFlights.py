from flask import Flask, request, Response
from skyscanner.skyscanner import Flights
from rdflib import Graph
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Messages.FlightRequestMessage import FlightRequestMessage
from PracticaECSDI.Messages.FlightResponseMessage import FlightResponseMessage
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants

app = Flask(__name__)
service = None


@app.route('/comm', methods=['GET', 'POST'])
def comm():
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.FLIGHT_REQUEST:
        flights = getFlights(graph)
        return flights.serialize()
    else:
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)

@app.route('/itstime', methods=['GET', 'POST', 'PUT'])
def time_to_send():
    return service.time_to_send()

def getFlights(graph):
    infoFlight = Flights.FlightMessage.from_graph(graph)
    maxprice = infoFlight.maxprice
    initdate = infoFlight.initdate
    finaldate = infoFlight.finaldate
    fromcity = infoFlight.fromcity
    tocity = infoFlight.tocity

    # GO TO SKYSCANER and get the vuelos anda i tornada
    # api-key: fi768769083827246592561385220425 (conta de cris)
    # https://skyscanner.github.io/slate/#browse-quotes
    # outboundPartialDate: (required) Format "yyyy-mm-dd", "yyyy-mm" or "anytime".
    # inboundPartialDate: (optional) Format "yyyy-mm-dd", "yyyy-mm" or "anytime". Use empty string for oneway trip.
    # examples: https://skyscanner.readthedocs.io/en/latest/usage.html

    flights_service = Flights('fi768769083827246592561385220425')

    if fromcity == 'Barcelona':
        fromCity = 'BCN'
        count = 'ES'
    elif fromcity == 'Paris':
        fromCity = 'PARI'
        count = 'FR'
    elif fromcity == 'Londres':
        fromCity = 'LOND'
        count = 'UK'
    """elif fromcity == 'Madrid':
        fromCity = 'MAD'
        count = 'ES'
    elif fromcity == 'Estocolm':
        fromCity = 'STOC'
        count = 'SE'
    elif fromcity == 'Milan':
        fromCity = 'Mila'
        count = 'IT'"""

    """ result = flights_service.get_result(
    country=count,
    currency='EUR',
    locale='es-ES',
    originplace=fromCity,
    destinationplace=toCity,
    outbounddate=initdate,
    inbounddate=finaldate,
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

    #return result

    return "FLights response"


if __name__ == '__main__':
    app.run(port=Constants.PORT_AFlights, debug=True)
