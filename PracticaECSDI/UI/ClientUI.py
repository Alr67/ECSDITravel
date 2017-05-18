import sys
import requests
from datetime import date
from Constants import Ontologies, FIPAACLPerformatives, Constants
from AgentUtil.ACLMessages import build_message
from Messages.FlightMessage import FlightMessage
from Messages.ActivitiesRequestMessage import ActivitiesRequestMessage

LocalhostUrl = "http://127.0.0.1:"

def configUrls():
    configOption = -1
    while configOption != 0:
        print "0. No"
        print "1. Si"
        configOption = raw_input("Quieres definir las url de los agentes?")
        print
        try:
            configOption = int(configOption)
            if configOption not in [0, 1]:
                print ("Opcion incorrecta")
            else:
                if configOption == 0:
                    break
                if configOption == 1:
                    AFlightUrl = askForString("Url/ip del agente de vuelos: ")
                    print "Url/ip del agente de vuelos que usara el sistema: " + AFlightUrl
                    print
                    return
        except ValueError:
            print "El valor ha de ser numerico"
        print

def askActivitiesData():
    print 'Tell me about your activities'
    maxPrice = askForInt("Max price: ")
    print 'Max price to request: ', maxPrice
    activities_url = LocalhostUrl + str(Constants.PORT_AActivities) + "/comm"
    print 'url: ', activities_url
    initDate = date(2011,11,17)
    finDate = date(2011,11,24)
    messageData = ActivitiesRequestMessage(1, initDate,finDate,maxPrice)
    gra = messageData.to_graph()
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.ACTIVITIES_REQUEST).serialize(format='xml')

    resp = requests.post(activities_url, data=dataContent)
    print 'he tornat a la consola clientUI'
    print resp


    return

def askFlightsData():
    print 'Tell me about your flights'
    maxPrice = askForString("Max price: ")
    print 'Max price to request: ', maxPrice
    flightsAgent = LocalhostUrl + str(Constants.PORT_AFlights) + "/comm"
    print 'url: ', flightsAgent
    messageData = FlightMessage(1, maxPrice)
    print 'data normal:'
    print messageData
    print 'data graph:'
    gra = messageData.to_graph()
    print gra
    print 'finish data'
    dataContent = build_message(gra, FIPAACLPerformatives.REQUEST, Ontologies.FLIGHT_REQUEST).serialize(format='xml')

    resp = requests.post(flightsAgent, data=dataContent)
    print 'he tornat a la consola clientUI'
    print resp

def askHotelData():
    print 'Tell me about your hotels'
    return

def main():
    #askFlightsData()
    askActivitiesData()
    #askHotelData()


def main1():
    username = askForString("Nombre del usuario que usara el sistema: ")

    option = -1
    while option != 0:
        print "0. Salir"
        print "1. Buscar vuelo"
        print "2. Buscar alojamiento (TODO)"
        print "3. Buscar completo vuelo + alojamiento (TODO)"
        print "4. Buscar actividades (TODO)"
        print "5. Buscar completo (TODO)"

        option = raw_input("Escoge una opcion: ")
        print
        try:
            option = int(option)
            if option not in [1, 2, 3, 4, 5]:
                print ("Opcion incorrecta")
            else:
                if option == 1:
                    askFlightsData()
                    return
                if option == 2:
                    askHotelData()
                    return
                if option == 3:
                    return
                if option == 4:
                    return
                if option == 5:
                    return
        except ValueError:
            print "Este valor ha de ser numerico"
        print


def askForString(message):
    response = raw_input(message)
    while response.strip().find(" ") != -1:
        print "No puede contener espacios"
        response = raw_input(message)
        return response

def askForInt(message):
    while True:
        try:
            response = eval(raw_input(message))
            return response
        except:
            pass
            print("Not an integer value...")


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    # print "USAGE: python UserInteface {AUSER_URI} {APURCHASES_URI}"
    # exit(-1)
    # auser = sys.argv[1]
    # apurchases = sys.argv[2]
    # cart = {}
    main()
