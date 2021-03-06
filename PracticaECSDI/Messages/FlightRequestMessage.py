from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants


class FlightRequestMessage:
    def __init__(self, uuid, maxprice, initDate, finalDate, departureAirport, arrivalAirport):
        self.uuid = uuid
        self.maxPrice = maxprice
        self.firstDay = initDate
        self.lastDay = finalDate
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        flight = namespace.__getattr__('#RequestFlight#' + str(self.uuid))
        graph.add((flight, FOAF.Uuid, Literal(self.uuid)))
        graph.add((flight, FOAF.MaxPrice, Literal(self.maxPrice)))
        graph.add((flight, FOAF.FirstDay, Literal(self.firstDay)))
        graph.add((flight, FOAF.LastDay, Literal(self.lastDay)))
        graph.add((flight, FOAF.DepartureAirport, Literal(self.departureAirport)))
        graph.add((flight, FOAF.ArrivalAirport, Literal(self.arrivalAirport)))
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?uuid ?maxPrice ?firstDay ?lastDay ?arrivalAirport ?departureAirport
           WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:MaxPrice ?maxPrice.
                ?x ns1:FirstDay ?firstDay.
                ?x ns1:LastDay ?lastDay.
                ?x ns1:DepartureAirport ?departureAirport.
                ?x ns1:ArrivalAirport ?arrivalAirport
           }
        """
        qres = graph.query(query)
        search_res = []
        for f, uuid, maxprice, firstDay, lastDay, arrivalAirport, departureAirport in qres:
            """search_res.append(FlightMessage(
                uuid.toPython(),
                maxprice.toPython(),
                firstDay.toPython(),
                lastDay.toPython(),
                departureAirport.toPython(),
                arrivalAirport.toPython()
            ))"""
            return FlightRequestMessage(uuid.toPython(), maxprice.toPython(), firstDay.toPython(), lastDay.toPython(),
                                        departureAirport.toPython(),arrivalAirport.toPython())
        #return search_res
