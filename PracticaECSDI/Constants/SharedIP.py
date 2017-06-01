
class DistributedIP:
    def __init__(self):
        self.flights_IP = "http://127.0.0.1:"
        self.acommodation_IP = "http://127.0.0.1:"
        self.activities_IP = "http://127.0.0.1:"
        self.payment_IP = "http://127.0.0.1:"

    def __str__(self):
        return self.flights_IP
    # FLIGHTS #
    def change_flights_IP(self, newIP):
        assert isinstance(newIP, str)
        self.flights_IP = newIP

    def get_flights_IP(self):
        return self.flights_IP
    ################
    # ACOMM #
    def change_acommodation_IP(self, newIP):
        assert isinstance(newIP, str)
        self.acommodation_IP = newIP

    def get_acommodation_IP(self):
        return self.acommodation_IP
    ###################
    # ACT ############
    def change_activities_IP(self, newIP):
        assert isinstance(newIP, str)
        self.activities_IP = newIP

    def get_activities_IP(self):
        return self.activities_IP
    ###############
    #PAYM##########
    def change_payment_IP(self, newIP):
        assert isinstance(newIP, str)
        self.payment_IP = newIP

    def get_payment_IP(self):
        return self.flights_IP
    ###########
disIP = DistributedIP()