from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants

class AcommodationRequestMessage:
    def __init__(self,id,initDate,finalDate,maxPrice,city):
        self.uuid = id
        self.firstDay = initDate
        self.lastDay = finalDate
        self.maxPrice = maxPrice
        self.city = city

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        acomm = namespace.__getattr__('#RequestAcommodation#'+str(self.uuid))
        graph.add((acomm,FOAF.Uuid,Literal(self.uuid)))
        graph.add((acomm,FOAF.MaxPrice,Literal(self.maxPrice)))
        graph.add((acomm,FOAF.FirstDay,Literal(self.firstDay)))
        graph.add((acomm,FOAF.LastDay,Literal(self.lastDay)))
        graph.add((acomm,FOAF.City, Literal(self.city)))
        return graph

    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?maxPrice ?firstDay ?lastDay ?city
            WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:MaxPrice ?maxPrice.
                ?x ns1:FirstDay ?firstDay.
                ?x ns1:LastDay ?lastDay
                ?x ns1:City ?city
            }
        """
        resp = graph.query(query)
        for f,uuid,maxprice,firstDay,lastDay,city in resp:
            return AcommodationRequestMessage(uuid.toPython(),firstDay.toPython(), lastDay.toPython(),maxprice.toPython(), city.toPython())