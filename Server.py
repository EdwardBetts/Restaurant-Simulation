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
        self.lastOpenTime = Time.Time(seconds = 0)
        self.lastCloseTime = None
        self.totalOpenTime = 0
        self.totalUtilizationTime = 0
        self.lastCustomerArrivedTime = None
        
        #Additional servers are added for rush times
        self.rushHour = False
        self.closed = False
        
    def isAdditional(self):
        return self.rushHour
    
    def isBusy(self):
        return self.busy
    
    #Close the additional server and record info
    def close(self, currentTime):
        self.closed = True
        self.totalOpenTime += self.lastOpenTime.timeDiff(currentTime)
        self.lastCloseTime = Time.Time(currentTime)
        self.totalOpenTime += self.lastOpenTime.timeDiff(currentTime)
        
    def getOpenTime(self, currentTime):
        if self.closed:
            return self.totalOpenTime
        else:
            return self.totalOpenTime + self.lastOpenTime.timeDiff(currentTime)
    
    def getUtilizationTime(self, currentTime):
        if self.busy:
            return self.utilizationTime + self.lastCustomerArrivedTime.timeDiff(currentTime)
        else:
            return self.utilizationTime
    
    def assignCustomer(self, newCust, currentTime):
        self.busy = True
        newTime = Time.Time(currentTime)
        newTime.addSeconds(newCust.serviceTime)
        self.releaseTime = newTime
        self.cust = newCust
        self.lastCustomerArrivedTime = Time.Time(currentTime)
        
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