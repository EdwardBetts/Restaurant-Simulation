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
        self.foodWaitTime = self.setFoodWaitTime()
        self.foodDeliveryTime = None
        self.queueTime = 0
    
    def getServiceTime(self):
        serviceTime = int(random.expovariate(1.0/(inputs.serviceTimeMeanMinutes*60.0)))
        while serviceTime == 0:
            serviceTime = int(random.expovariate(1.0/(inputs.serviceTimeMeanMinutes*60.0)))
        return serviceTime
    
    def printInfo(self):
        print "Customer id: #{idNum}".format(idNum = custID)
        print "Service time: {st}".format(st = self.serviceTime)
        print "Arrival time: {at}".format(at = self.arrivalTime.printInfo())
        
    def setFoodWaitTime(self):
        food = int(random.expovariate(1.0/(inputs.foodTimeWaitMeanMinutes*60.0)))
        while food == 0:
            food = int(random.expovariate(1.0/(inputs.foodTimeWaitMeanMinutes*60.0)))
        return food
    
    def setFoodDeliveryTime(self, currentTime):
        newTime = Time.Time(currentTime)
        newTime.addSeconds(self.foodWaitTime)
        self.foodDeliveryTime = newTime