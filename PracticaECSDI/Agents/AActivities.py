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
    graph = Graph().parse(data=request.data, format='xml')
    ontology = ACLMessages.get_message_ontology(graph)
    if ontology == Ontologies.SEND_ACTIVITIES_REQUEST:
        message = processActivitiesRequest(graph)
        return message
    else:
        print 'I dont understand'
        return ACLMessages.build_message(Graph(),
            FIPAACLPerformatives.NOT_UNDERSTOOD,
            Ontologies.UNKNOWN_ONTOLOGY)

def processActivitiesRequest(graph):
    print 'im in get activities from graph'
    data = ActivitiesRequestMessage.from_graph(graph)
    print  'initDate: ',data.firstDay
    print  'lastDay: ',data.lastDay
    print 'location: ',data.location
    print 'type: ',data.type
    planList = askGooglePlaces(data.location,data.type, data.firstDay,data.lastDay)
    print 'plan length: ',len(planList)
    return processActivitiesPlan(planList)
def initGooglePlacesApiParams():
    with open('../config.json') as json_data:
        d = json.load(json_data)
        json_data.close()
        print(d)
        API_KEY = d["API_KEY_GOOGLE"]
        print "apikey:"+ API_KEY
        global google_places
        google_places = GooglePlaces(API_KEY)#, types, API_KEY
    return
def askGooglePlaces(location,type,firstDay,lastDay):
    initGooglePlacesApiParams()
    query_result = google_places.nearby_search(location=location,radius=20000,types=[type])
    if query_result.has_attributions:
        print query_result.html_attributions
    return processGooglePlacesResult(query_result.places,firstDay,lastDay)
def processGooglePlacesResult(arrayPlaces, firstDay, lastDay):
    days = (lastDay-firstDay).days
    print 'days: ',days
    num = 0
    planList = []
    for i in range(days):
        print ' montant dia ',i
        dayPlan = DayPlan(i, firstDay + datetime.timedelta(days=i))
        dayPlan.activity1 = arrayPlaces[num].name
        num = num +1
        dayPlan.activity2 = arrayPlaces[num].name
        num = num +1
        dayPlan.activity3 = arrayPlaces[num].name
        num = num +1
        planList.append(dayPlan)
    return  planList
def processActivitiesPlan(planList):
    responseObj = ActivitiesResponseMessage(1, planList)
    # TO-ASK: Cal ontologia de resposta tambe??? O amb performativa ja n'hi ha prou?
    dataContent = build_message(responseObj.to_graph(), FIPAACLPerformatives.AGREE,
                                Ontologies.SEND_ACTIVITIES_RESPONSE).serialize(format='xml')
    return dataContent

def exampleProcessArray(arrayplaces):
    for place in arrayplaces:
        print 'Im processing array results n',num
        num = num+1
        # Returned places from a query are place summaries.
        pl = GooglePlacesAct(place)
        pl.printData()
        print "letsget more detail"
            # The following method has to make a further API call.
        place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        print "details: ",place.details # A dict matching the JSON response from Google.
        #             print place.local_phone_number
        print "phonenumber: ",place.international_phone_number
        print "website: ",place.website
        print "url: ",place.url


            # Getting place photos
        #getDetailPhotos(place.photos)

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

def get_file(path):
    f = open(path, 'r')
    output = f.read()
    f.close()
    return output


class GooglePlacesAct:
    def __init__(self,place):
        self.name = place.name
        self.geo_location = place.geo_location
        self.place_id = place.place_id

    def printData(self):
        print "Activity: "
        print "     Name: ", self.name
        print "     Location: ",self.geo_location
        print "     PlaceId: ",self.place_id

    def addDetail(self,details):
        return

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=Constants.PORT_AActivities, debug=True)


