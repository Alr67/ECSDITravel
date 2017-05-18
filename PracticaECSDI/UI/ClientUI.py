import sys
import requests
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from PracticaECSDI.Messages import ConsoleMessage
AFlightUrl = "http://127.0.0.1:"

def configUrls():
    configOption = -1
    while configOption != 0:
        print "0. No"
        print "1. Si"
        configOption = raw_input("Quieres definir las url de los agentes?")
        print
        try:
            configOption = int(configOption)
            if configOption not in [0,1]:
                print ("Opcion incorrecta")
            else:
                if configOption == 0:
                    break
                if configOption == 1:
                    AFlightUrl = askForString("Url/ip del agente de vuelos: ")
                    print "Url/ip del agente de vuelos que usara el sistema: "+AFlightUrl
                    print
                    return
        except ValueError:
            print "El valor ha de ser numerico"
        print

def askFlightsData():
    maxPrice = askForString("Max price: ")
    #print "Max price to request: "+ maxPrice
    flightsAgent= AFlightUrl+Constants.PORT_AFlights + "/comm"
    messageData = ConsoleMessage(1,maxPrice)
    resp = requests.post(flightsAgent,data= build_message(messageData.to_graph(),FIPAACLPerformatives.QUERY_IF, Ontologies.FLIGHT_REQUEST).serialize(format="xml"))
    return

def askHotelData():
    return

def askForString(message):
    response = raw_input(message)
    while response.strip().find(" ") != -1:
        print "No puede contener espacios"
        response = raw_input(message)
        return response

def data_ToGraph():

    return

def main():
    askFlightsData()



    configUrls()

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
            if option not in [0, 1, 2, 3, 4, 5]:
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


if __name__ == "__main__":
    #if len(sys.argv) != 3:
        #print "USAGE: python UserInteface {AUSER_URI} {APURCHASES_URI}"
        #exit(-1)
    #auser = sys.argv[1]
    #apurchases = sys.argv[2]
    #cart = {}
    main()
