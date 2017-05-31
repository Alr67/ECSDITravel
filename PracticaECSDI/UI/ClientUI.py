from PracticaECSDI.Utils.UtilAcommodation import askHotelData
from PracticaECSDI.Utils.UtilActivities import askActivitiesData
from PracticaECSDI.Utils.UtilDecisiones import askPlanData
from PracticaECSDI.Utils.UtilFlights import askFlightsData
from PracticaECSDI.Utils.UtilGeneral import askForString
from PracticaECSDI.Utils.UtilPayment import askPaymentData


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
                askPaymentData()
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
    username = askForString("Nombre del usuario que usara el sistema: ")

    option = -1
    while option != 0:
        print "\nEscoge una opcion: "
        print "0. Salir"
        print "1. Iniciar planificacion viaje"
        print "2. Pagar viaje\n"

        option = raw_input("")
        try:
            option = int(option)
            if option not in [0,1, 2]:
                print ("Opcion incorrecta")
            else:
                if option == 1:
                    askPlanData()
                if option == 2:
                    askPayment()
                if option == 0:
                    return
        except ValueError:
            print "Este valor debe ser numerico\n"


def main1():
    username = askForString("Nombre del usuario que usara el sistema: ")

    option = -1
    while option != 0:
        print "\nEscoge una opcion: "
        print "0. Salir"
        print "1. Buscar completo vuelo + alojamiento"
        print "2. Buscar actividades (TODO)"
        print "3. Pagar viaje"
        print "4. Buscar completo (TODO)\n"

        option = raw_input("")
        try:
            option = int(option)
            if option not in [1, 2, 3, 4]:
                print ("Opcion incorrecta")
            else:
                if option == 1:
                    askPlanData()
                if option == 2:
                    askActivitiesData()
                if option == 3:
                    askPayment()
                if option == 4:
                    return
        except ValueError:
            print "Este valor debe ser numerico\n"


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    # print "USAGE: python UserInteface {AUSER_URI} {APURCHASES_URI}"
    # exit(-1)
    # auser = sys.argv[1]
    # apurchases = sys.argv[2]
    # cart = {}
    #main1()
    main()
