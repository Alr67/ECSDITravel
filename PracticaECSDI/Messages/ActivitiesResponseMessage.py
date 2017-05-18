from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants

class ActivitiesResponseMessage:
    def __init__(self,id,activities):
        #llista de dies amb les corresponents activitats
        self.day_activities = activities
        self.uuid = id

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        prod = namespace.__getattr__('#RequestActivities#'+str(self.uuid))
        graph.add((prod,FOAF.Uuid,Literal(self.uuid)))
        graph.add((prod,FOAF.DayActivities,Literal(self.day_activities)))
        return graph

    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?day_activities
            WHERE {
                ?x ns1:Uuid ?uuid.
                ?x ns1:DayActivities ?day_activities
            }
        """
        resp = graph.query(query)
        for f,uuid,day_activities in resp:
            return ActivitiesResponseMessage(uuid.toPython(),day_activities.toPython(),)