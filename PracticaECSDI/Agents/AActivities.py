from flask import Flask, request, Response
from rdflib import Graph
import datetime
from PracticaECSDI.AgentUtil import ACLMessages
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.Messages.ActivitiesRequestMessage import ActivitiesRequestMessage
from PracticaECSDI.Messages.ActivitiesResponseMessage import ActivitiesResponseMessage,DayPlan
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from googleplaces import GooglePlaces, types, lang
import json
import os

google_places = ""
app = Flask(__name__)
service = None

@app.route('/comm', methods=['GET', 'POST'])
def comm():
    print 'Im in Activities Agent, comm function'
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_ACTIVITIES_REQUEST:
        print 'Its a activity request'
        message = getActivities(graph)
        print 'activities graph obtained, lets construct response message'
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(), FIPAACLPerformatives.NOT_UNDERSTOOD, Ontologies.UNKNOWN_ONTOLOGY)

def initGooglePlaces():
    with open('../config.json') as json_data:
        d = json.load(json_data)
        json_data.close()
        print(d)
        API_KEY = d["API_KEY_GOOGLE"]
        print "apikey:"+ API_KEY
        global google_places
        google_places = GooglePlaces(API_KEY)
    return

def processGooglePlacesResult(arrayplaces):
    for place in arrayplaces:
        # Returned places from a query are place summaries.
        pl = GooglePlacesAct(place)
        pl.printData()

            # The following method has to make a further API call.
        place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        print place.details # A dict matching the JSON response from Google.
        #             print place.local_phone_number
        print place.international_phone_number
        print place.website
        print place.url
        break

            # Getting place photos
        #getDetailPhotos(place.photos)

def askGooglePlaces(location):
    initGooglePlaces()
    query_result = google_places.nearby_search(location='London, England', keyword='Fish and Chips',radius=20000, types=[types.TYPE_FOOD])
    if query_result.has_attributions:
        print query_result.html_attributions
    processGooglePlacesResult(query_result.places)


def getDetailPhotos(photosarray):
    for photo in photosarray:
        # 'maxheight' or 'maxwidth' is required
        photo.get(maxheight=500, maxwidth=500)
            # MIME-type, e.g. 'image/jpeg'
        photo.mimetype
                # Image URL
        photo.url
                # Original filename (optional)
        photo.filename
                # Raw image data
        photo.data

def askGooglePlaces2(location):
    data_file = get_file('../config.json')
    print 'data',data_file
    data = json.JSONDecoder.decode(data_file)
    API_KEY = data["API_KEY_GOOGLE"]
    print "apikey:"+ API_KEY
    return

def get_file(path):
    f = open(path, 'r')
    output = f.read()
    f.close()
    return output

def getActivities(graph):
    askGooglePlaces("1")
    print 'im in get activities from graph'
    data = ActivitiesRequestMessage.from_graph(graph)
    print 'data obtained: ',data
    print  'initDate: ',data.firstDay
    print  'lastDay: ',data.lastDay
    print  'maxPrice: ',data.maxPrice
    days = (data.lastDay-data.firstDay).days
    print 'days: ',days
    planList = []
    for i in range(days):
        dayPlan = DayPlan(i,data.firstDay+ datetime.timedelta(days=i),"Pending","Pending","Pending")
        planList.append(dayPlan)
    print 'plan length: ',len(planList)
    responseObj = ActivitiesResponseMessage(1,planList)
    #TO-ASK: Cal ontologia de resposta tambe??? O amb performativa ja n'hi ha prou?
    dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE, Ontologies.SEND_ACTIVITIES_RESPONSE).serialize(format='xml')
    return dataContent


if __name__ == '__main__':
    app.run(port=Constants.PORT_AActivities, debug=True)

class GooglePlacesAct:
    def __init__(self,place):
        self.name = place.name
        self.geo_location = place.geo_location
        self.place_id = place.place_id

    def printData(self):
        print self.name
        print self.geo_location
        print self.place_id

    def addDetail(self,details):
        return

