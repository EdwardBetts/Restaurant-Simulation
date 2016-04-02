import random
import itertools
import inputs
import Time

class Customer(object):
    
    custID = itertools.count().next
    
    def __init__(self, currentTime):
        self.serviceTime = self.getServiceTime()
        self.arrivalTime = Time.Time(timeObject = currentTime)
        self.custID = Customer.custID() + 1
    
    def getServiceTime(self):
        return random.expovariate(1.0/inputs.serviceTimeMean)
    
    def printInfo(self):
        print "Customer id: #{idNum}".format(idNum = custID)
        print "Service time: {st}".format(st = self.serviceTime)
        print "Arrival time: {at}".format(at = self.arrivalTime.printInfo())