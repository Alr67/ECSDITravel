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
