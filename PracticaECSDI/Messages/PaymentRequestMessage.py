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
        graph.add((pay, FOAF.name, Literal(self.name)))
        graph.add((pay, FOAF.card, Literal(self.card)))
        graph.add((pay, FOAF.ammount, Literal(self.amount)))
        return graph

    @classmethod
    def from_graph(cls, graph):
        query = """SELECT ?x ?name ?card ?amount
            WHERE {
                ?x ns1:name ?name.
                ?x ns1:card ?card.
                ?x ns1:amount ?amount.
            }
        """
        resp = graph.query(query)
        for f, name, card, amount in resp:
            return PaymentRequestMessage(name.toPython(), card.toPython(), amount.toPython())

