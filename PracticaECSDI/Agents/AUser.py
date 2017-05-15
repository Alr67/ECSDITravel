import sys
AFlightUrl = "someUrl"


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

                    url = raw_input("Url/ip del agente de vuelos: ")
                    while url.strip().find(" ") != -1:
                        print "No puede contener espacios"
                        url = raw_input("Url/ip del agente de vuelos: ")
                    AFlightUrl = url
                    print "Url/ip del agente de vuelos que usara el sistema: "+AFlightUrl
                    print
                    return
        except ValueError:
            print "El valor ha de ser numerico"
        print

def main():
    configUrls()

    username = raw_input("Nombre del usuario que usara el sistema: ")
    while username.strip().find(" ") != -1:
        print "El nombre de usuario no puede contener espacios"
        username = raw_input("Nombre del usuario que usara el sistema: ")

    option = -1
    while option != 0:
        print "0. Salir"
        print "1. Buscar viaje"
        print "2. Ir a la cesta de la compra"
        print "3. Devolver un producto"
        print "4. Consultar compras"
        option = raw_input("Escoge una opcion: ")
        print
        try:
            option = int(option)

            if option not in [0, 1, 2, 3, 4]:
                print ("Opcion incorrecta")
            else:
                if option == 1:
                    return
                if option == 2:
                    return
                if option == 3:
                    return
                if option == 4:
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
