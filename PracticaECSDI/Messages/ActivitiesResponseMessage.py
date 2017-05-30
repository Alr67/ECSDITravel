from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants

class ActivitiesResponseMessage:
    def __init__(self,id,activities):
        #llista de dies amb les corresponents activitats
        self.day_plans = activities
        self.uuid = id

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        prod = namespace.__getattr__('#ResponseActivities#'+str(self.uuid))
        graph.add((prod,FOAF.Uuid,Literal(self.uuid)))
        graph.add((prod,FOAF.DayPlans,Literal(self.day_plans)))
        for day in self.day_plans:
            graph = graph + self.l_to_graph(day)
        return graph

    def l_to_graph(self,day):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        pd = namespace.__getattr__('#DayActivity#' + str(day.uuid))
        graph.add((pd, FOAF.Uuid2, Literal(day.uuid)))
        graph.add((pd, FOAF.Date, Literal(day.date)))
        graph.add((pd, FOAF.Activity1, Literal(day.activity1)))
        graph.add((pd, FOAF.Activity2, Literal(day.activity2)))
        graph.add((pd, FOAF.Activity3, Literal(day.activity3)))
        return graph

    @classmethod
    def from_graph(cls,graph):
        query = """SELECT ?x ?uuid ?activity1 ?activity2 ?activity3 ?date
                    WHERE {
                        ?x ns1:Uuid2 ?uuid.
                        ?x ns1:Activity1 ?activity1.
                        ?x ns1:Activity2 ?activity2.
                        ?x ns1:Activity3 ?activity3.
                        ?x ns1:Date ?date
                    }
                """
        day = graph.query(query)
        days = []
        for f,uuid,activity1,activity2,activity3,date in day:
            new = DayPlan(uuid.toPython(),date.toPython())
            new.activity1 = activity1.toPython()
            new.activity2 = activity2.toPython()
            new.activity3 = activity3.toPython()
            days.append(new)

        query = """SELECT ?x ?uuid
                    WHERE {
                        ?x ns1:Uuid ?uuid.
                    }
                """
        resp = graph.query(query)
        for f,uuid in resp:
            return ActivitiesResponseMessage(uuid.toPython(),days)

class DayPlan:
    def __init__(self,id,date,activity1,activity2,activity3):
        #llista de dies amb les corresponents activitats
        self.activity1 = activity1
        self.activity2 = activity2
        self.activity3 = activity3
        self.date = date
        self.uuid = id

    def __init__(self,id,date):
        #llista de dies amb les corresponents activitats
        self.date = date
        self.uuid = id
