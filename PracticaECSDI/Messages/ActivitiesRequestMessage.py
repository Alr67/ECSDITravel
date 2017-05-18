from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from Constants import Ontologies, FIPAACLPerformatives, Constants

class ActivitiesRequestMessage:
    def __init__(self,id,initDate,finalDate, maxPrice):
        self.uuid = id
        self.firstDay = initDate
        self.lastDay = finalDate
        self.maxPrice = maxPrice

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        prod = namespace.__getattr__('#RequestActivities#'+str(self.uuid))
        graph.add((prod,FOAF.Uuid,Literal(self.uuid)))
        graph.add((prod,FOAF.MaxPrice,Literal(self.maxPrice)))
        graph.add((prod,FOAF.FirstDay,Literal(self.firstDay)))
        graph.add((prod,FOAF.LastDay,Literal(self.lastDay)))
        return graph

    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?maxprice ?firstDay ?lastDay
            WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:MaxPrice ?maxPrice.
                ?x ns1:FirstDay ?firstDay.
                ?x ns1:LastDay ?lastDay
            }
        """
        resp = graph.query(query)
        for f,uuid,maxprice,firstDay, lastDay in resp:
            return ActivitiesRequestMessage(uuid.toPython(),firstDay.toPython(), lastDay.toPython(),maxprice.toPython())
