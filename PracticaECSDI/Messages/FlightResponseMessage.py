from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants


class FlightResponseMessage:
    def __init__(self, uuid, price, idflightgo, companygo, departurehourgo,arrivalhourgo,idflightback, companyback, departurehourback,arrivalhourback):
        self.uuid = uuid
        self.price = price
        self.idflightgo = idflightgo
        self.companygo = companygo
        self.departurehourgo = departurehourgo
        self.arrivalhourgo = arrivalhourgo
        self.idflightback = idflightback
        self.companyback = companyback
        self.departurehourback = departurehourback
        self.arrivalhourback = arrivalhourback

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        flight = namespace.__getattr__('#ResponseFlight#' + str(self.uuid))
        graph.add((flight, FOAF.Uuid, Literal(self.uuid)))
        graph.add((flight, FOAF.Price, Literal(self.price)))
        graph.add((flight, FOAF.IdFlightGo, Literal(self.idflightgo)))
        graph.add((flight, FOAF.CompanyGo, Literal(self.companygo)))
        graph.add((flight, FOAF.DepartureHourGo, Literal(self.departurehourgo)))
        graph.add((flight, FOAF.ArrivalHourGo, Literal(self.arrivalhourgo)))
        graph.add((flight, FOAF.IdFlightBack, Literal(self.idflightback)))
        graph.add((flight, FOAF.CompanyBack, Literal(self.companyback)))
        graph.add((flight, FOAF.DepartureHourBack, Literal(self.departurehourback)))
        graph.add((flight, FOAF.ArrivalHourBack, Literal(self.arrivalhourback)))
        return graph

    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?price ?idflightgo ?companygo ?departurehourgo ?arrivalhourgo ?idflightback ?companyback ?departurehourback ?arrivalhourback
                    WHERE {
                        ?x ns1:Uuid ?uuid.
                        ?x ns1:Price ?price.
                        ?x ns1:IdFlightGo ?idflightgo.
                        ?x ns1:CompanyGo ?companygo.
                        ?x ns1:DepartureHourGo ?departurehourgo.
                        ?x ns1:ArrivalHourGo ?arrivalhourgo.
                        ?x ns1:IdFlightBack ?idflightback.
                        ?x ns1:CompanyBack ?companyback.
                        ?x ns1:DepartureHourBack ?departurehourback.
                        ?x ns1:ArrivalHourBack ?arrivalhourback
                    }
                """
        flight = graph.query(query)
        resp = []

        for f,uuid,price,idflightgo,companygo,departurehourgo,arrivalhourgo,idflightback,companyback,departurehourback,arrivalhourback in flight:
            """resp.append(FlightMessage(
                            uuid.toPython(),
                            price.toPython(),
                            idflightgo.toPython(),
                            companygo.toPython(),
                            departurehourgo.toPython(),
                            arrivalhourgo.toPython(),
                            idflightgo.toPython(),
                            companygo.toPython(),
                            departurehourgo.toPython(),
                            arrivalhourgo.toPython()
                        ))"""
            return FlightResponseMessage(uuid.toPython(), price.toPython(), idflightgo.toPython(),
                                         companygo.toPython(), departurehourgo.toPython(), arrivalhourgo.toPython(),
                                         idflightback.toPython(),companyback.toPython(), departurehourback.toPython(),
                                         arrivalhourback.toPython())

        #return resp

