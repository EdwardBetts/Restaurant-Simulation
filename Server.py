import itertools
import Time

class Server(object):
    
    serverID = itertools.count().next
    
    def __init__(self):
        self.utilizationTime = 0
        self.busy = False
        self.cust = None
        self.releaseTime = None
        self.serverID = Server.serverID() + 1
    
    def isBusy(self):
        return self.busy
    
    def getUtilizationTime(self):
        return self.utilizationTime
    
    def assignCustomer(self, newCust, currentTime):
        self.busy = True
        newTime = Time.Time(currentTime)
        newTime.addSeconds(newCust.serviceTime)
        self.releaseTime = newTime
        self.cust = newCust
        
    def releaseCustomer(self):
        self.busy = False
        self.utilizationTime += self.cust.serviceTime
        self.releaseTime = None
        self.cust = None
        
    def printInfo(self):
        print "Server ID:", self.serverID
        print "Busy?: ", self.busy
        if self.busy:
            print "self.releaseTime: ", self.releaseTime.stringInfo()