from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from Constants import Ontologies, FIPAACLPerformatives, Constants

class FlightMessage:
    def __init__(self,uuid,maxprice):
        self.uuid = uuid
        self.maxPrice = maxprice
    
    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        prod = namespace.__getattr__('#RequestFlight#'+str(self.uuid))
        graph.add((prod,FOAF.Uuid,Literal(self.uuid)))
        graph.add((prod,FOAF.MaxPrice,Literal(self.maxPrice)))
        return graph
