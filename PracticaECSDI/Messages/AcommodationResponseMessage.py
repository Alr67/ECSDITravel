from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants

class AcommodationResponseMessage:
    def __init__(self,id,hotelName, hotelPrice, hotelStreet):
        #llista de dies amb les corresponents activitats
        self.name = hotelName
        self.uuid = id
        self.price = hotelPrice
        self.street = hotelStreet

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        prod = namespace.__getattr__('#ResponseAcommodation#'+str(self.uuid))
        graph.add((prod,FOAF.Uuid,Literal(self.uuid)))
        graph.add((prod,FOAF.Price,Literal(self.price)))
        graph.add((prod, FOAF.Name, Literal(self.name)))
        graph.add((prod, FOAF.Street, Literal(self.street)))
        return graph


    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?hotelName ?hotelPrice ?hotelStreet
                    WHERE {
                        ?x ns1:Uuid ?uuid.
                        ?x ns1:HotelName ?hotelName.
                        ?x ns1:HotelPrice ?hotelPrice.
                        ?x ns1:HotelStreet ?hotelStreet
                    }
                """
        resp = graph.query(query)
        for f, uuid, hotelName, hotelPrice, hotelStreet in resp:
            return AcommodationResponseMessage(uuid.toPython(), hotelName.toPython(), hotelPrice.toPython(),
                                               hotelStreet.toPython())

