from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants


class PaymentRequestMessage:
    def __init__(self, name, card, amount):
        self.name = name
        self.card = card
        self.amount = amount

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        pay = namespace.__getattr__('#RequestPayment#' + str(self.name))
        graph.add((pay, FOAF.Name, Literal(self.name)))
        graph.add((pay, FOAF.Card, Literal(self.card)))
        graph.add((pay, FOAF.Ammount, Literal(self.amount)))
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?name ?card ?amount
            WHERE {
                ?x ns1:Name ?name.
                ?x ns1:Card ?card.
                ?x ns1:Amount ?amount
            }
        """
        resp = graph.query(query)
        for f, name, card, amount in resp:
            return PaymentRequestMessage(name.toPython(), card.toPython(), amount.toPython())
