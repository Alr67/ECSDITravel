import sys
import requests
from PracticaECSDI.Constants import Ontologies, FIPAACLPerformatives, Constants
from PracticaECSDI.AgentUtil.ACLMessages import build_message
from PracticaECSDI.Messages.FlightRequestMessage import FlightRequestMessage
from PracticaECSDI.Utils.UtilAcommodation import askHotelData
from PracticaECSDI.Utils.UtilFlights import askFlightsData
from PracticaECSDI.Utils.UtilGeneral import askForInt, askForString
from PracticaECSDI.Utils.UtilActivities import  askActivitiesData


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

def askHotelData():
    print 'Tell me about your hotels'
    return

def askPayment():
    print "\nEstas son las caracteristicas del viaje: dsdfsdfsdfsdfsdf"
    print "Quieres confirmar y pagar este viaje?"
    print "1. Si"
    print "2. No"
    print "3. Sinpa"

    try:
        option = raw_input("")
        option = int(option)
        if option not in [1, 2, 3, 4, 5]:
            print ("Opcion incorrecta")
        else:
            if option == 1:
                a = 1  # something
                return
            if option == 2:
                a = 1  # something
                return
            if option == 3:
                print "\nTu eres tonto?"
                return
    except ValueError:
        print "Este valor debe ser numerico"

def main():
    #askFlightsData()
    askActivitiesData()
    #askHotelData()


def main1():
    username = askForString("Nombre del usuario que usara el sistema: ")

    option = -1
    while option != 0:
        print "\nEscoge una opcion: "
        print "0. Salir"
        print "1. Buscar vuelo"
        print "2. Buscar alojamiento (TODO)"
        print "3. Buscar completo vuelo + alojamiento (TODO)"
        print "4. Buscar actividades (TODO)"
        print "5. Pagar viaje"
        print "6. Buscar completo (TODO)\n"

        option = raw_input("")
        try:
            option = int(option)
            if option not in [1, 2, 3, 4, 5, 6]:
                print ("Opcion incorrecta")
            else:
                if option == 1:
                    askFlightsData()
                if option == 2:
                    askHotelData()
                if option == 3:
                    a =  1 #something
                if option == 4:
                    askActivitiesData()
                if option == 5:
                    askPayment()
                if option == 6:
                    a = 1 #something
        except ValueError:
            print "Este valor debe ser numerico\n"


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    # print "USAGE: python UserInteface {AUSER_URI} {APURCHASES_URI}"
    # exit(-1)
    # auser = sys.argv[1]
    # apurchases = sys.argv[2]
    # cart = {}
    main1()
