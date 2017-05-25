from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants


class FlightResponseMessage:
    def __init__(self, uuid, idflight, price, company, departurehour,arrivalhour):
        self.uuid = uuid
        self.idflight = idflight
        self.price = price
        self.company = company
        self.departurehour = departurehour
        self.arrivalhour = arrivalhour

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        flight = namespace.__getattr__('#ResponseFlight#' + str(self.uuid))
        graph.add((flight, FOAF.Uuid, Literal(self.uuid)))
        graph.add((flight, FOAF.IdFlight, Literal(self.idflight)))
        graph.add((flight, FOAF.Price, Literal(self.price)))
        graph.add((flight, FOAF.Company, Literal(self.company)))
        graph.add((flight, FOAF.DepartureHour, Literal(self.departurehour)))
        graph.add((flight, FOAF.ArrivalHour, Literal(self.arrivalhour)))
        return graph

    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?idflight ?price ?company ?departurehour ?arrivalhour
                    WHERE {
                        ?x ns1:Uuid ?uuid.
                        ?x ns1:IdFlight ?idflight.
                        ?x ns1:Price ?price.
                        ?x ns1:Company ?company.
                        ?x ns1:DepartureHour ?departurehour.
                        ?x ns1:ArrivalHour ?arrivalhour
                    }
                """
        flight = graph.query(query)
        resp = []

        for f,uuid,idflight,price,company,departurehour,arrivalhour in flight:
            """resp.append(FlightMessage(
                            uuid.toPython(),
                            idflight.toPython()
                            price.toPython(),
                            company.toPython(),
                            departurehour.toPython()
                            arrivalhour.toPython()
                        ))"""
            return FlightResponseMessage(uuid.toPython(),idflight.toPython(), price.toPython(),
                                         company.toPython(), departurehour.toPython(), arrivalhour.toPython())

        #return resp

