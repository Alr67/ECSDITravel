from PracticaECSDI.Utils.UtilActivities import askActivitiesData
from PracticaECSDI.Utils.UtilDecisiones import askPlanData
from PracticaECSDI.Utils.UtilGeneral import askForString

AFlightURL = ""

#Constants.LocalhostUrl
def configUrls():
    configOption = -1
    while configOption != 0:
        print "Hola! Quieres ejecutarlo todo de manera local o distribuir los agentes?"
        print "0. No"
        print "1. Si"
        configOption = raw_input("")
        try:
            configOption = int(configOption)
            if configOption not in [0, 1]:
                print ("Opcion incorrecta")
            else:
                if configOption == 0:
                    print 'Todo local'
                    break
                if configOption == 1:
                    global AFlightURL
                    AFlightURL = askForString("Url/ip del agente de vuelos: ")
                    print "Url/ip del agente de vuelos que usara el sistema: " + AFlightURL
                    return
        except ValueError:
            print "El valor ha de ser numerico"

def main():
    username = askForString("Nombre del usuario que usara el sistema: ")

    configUrls()

    option = -1
    while option != 0:
        print "\nEscoge una opcion: "
        print "0. Salir"
        print "1. Iniciar planificacion viaje"

        option = raw_input("")
        try:
            option = int(option)
            if option not in [0, 1, 2]:
                print ("Opcion incorrecta")
            else:
                if option == 1:
                    askPlanData()
                if option == 0:
                    return
        except ValueError:
            print "Este valor debe ser numerico\n"



if __name__ == "__main__":
    main()
