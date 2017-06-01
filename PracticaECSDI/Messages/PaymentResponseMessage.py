from rdflib import Graph, Literal
from rdflib.namespace import Namespace, FOAF
from PracticaECSDI.Constants import Constants


class PaymentResponseMessage:
    def __init__(self, name, card, amount):
        self.name = name
        self.card = card
        self.amount = amount

    def to_graph(self):
        graph = Graph()
        namespace = Namespace(Constants.ONTOLOGY_NAME)
        prod = namespace.__getattr__('#ResponsePayment#'+str(self.name))
        graph.add((prod, FOAF.name, Literal(self.name)))
        graph.add((prod, FOAF.card, Literal(self.card)))
        graph.add((prod, FOAF.amount, Literal(self.amount)))
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
            return PaymentResponseMessage(name.toPython(), card.toPython(), amount.toPython())


def from_graph(graph):
    return None