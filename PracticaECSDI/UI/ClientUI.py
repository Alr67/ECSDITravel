from PracticaECSDI.Constants.SharedIP import disIP
from PracticaECSDI.Utils.UtilDecisiones import askPlanData
from PracticaECSDI.Utils.UtilGeneral import askForString


def configUrls():
    configOption = -1
    while configOption != 0:
        print "Hola! Quieres ejecutarlo todo de manera local o distribuir los agentes?"
        print "0. Local"
        print "1. Distribuida"
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
                    AFlightsURL = "http://"
                    AFlightsURL = AFlightsURL + raw_input("Dime la IP de Agente de vuelos")
                    AFlightsURL = AFlightsURL + ":"
                    disIP.change_flights_IP(AFlightsURL)
                    print "Url/ip del agente de vuelos que usara el sistema: ", disIP.flights_IP

                    AAcommURL = "http://"
                    AAcommURL = AAcommURL + raw_input("Dime la IP de Agente de hoteles")
                    AAcommURL = AAcommURL + ":"
                    disIP.change_acommodation_IP(AAcommURL)
                    print "Url/ip del agente de hoteles que usara el sistema: ", disIP.acommodation_IP

                    AActivURL = "http://"
                    AActivURL = AActivURL + raw_input("Dime la IP de Agente de actividades")
                    AActivURL = AActivURL + ":"
                    disIP.change_activities_IP(AActivURL)
                    print "Url/ip del agente de actividades que usara el sistema: ", disIP.activities_IP

                    APaymentURL = "http://"
                    APaymentURL = APaymentURL + raw_input("Dime la IP de Agente de pago")
                    APaymentURL = APaymentURL + ":"
                    disIP.change_payment_IP(APaymentURL)
                    print "Url/ip del agente de pago que usara el sistema: ", disIP.payment_IP
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
