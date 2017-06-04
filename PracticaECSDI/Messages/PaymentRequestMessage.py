from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants


class PaymentRequestMessage:
    def __init__(self,id, name, card, amount):
        self.uuid = id
        self.name = name
        self.card = card
        self.amount = amount

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        pay = namespace.__getattr__('#RequestPayment#' + str(self.uuid))
        graph.add((pay, FOAF.UuidP, Literal(self.uuid)))
        graph.add((pay, FOAF.NameP, Literal(self.name)))
        graph.add((pay, FOAF.CardP, Literal(self.card)))
        graph.add((pay, FOAF.AmountP, Literal(self.amount)))
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?uuid ?name ?card ?amount
            WHERE {
                ?x ns1:UuidP ?uuid.
                ?x ns1:NameP ?name.
                ?x ns1:CardP ?card.
                ?x ns1:AmountP ?amount
            }
        """
        resp = graph.query(query)
        print "resp: ",resp
        print "respcount: ",len(resp)
        for f, uuid, name, card, amount in resp:
            print "name: ",name
            print "card: ",card
            return PaymentRequestMessage(uuid.toPython(),name.toPython(), card.toPython(), amount.toPython())
        print "EndFor"
