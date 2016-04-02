import inputs
import Time
import Queue
import Server

class ServiceSystem(object):
    
    def __init__(self):
        self.numServers = inputs.numberOfServers
        self.numServersBusy = 0
        self.numServersAvailable = self.numServers
        self.queue = Queue.Queue()
        self.servers = []
        self.initializeServers()
        self.numCustomersServed = 0
        self.waitingForFood = []
        
    def initializeServers(self):
        for i in range(0, self.numServers):
            newServer = Server.Server()
            self.servers.append(newServer)
        
    def addCustomer(self, newCust, currentTime):
        timeString = currentTime.stringInfo()
        availableServer = self.findAvailableServer()
        if availableServer is not None:
            availableServer.assignCustomer(newCust, currentTime)
            print "  {t} Assigning customer #{cid} to server #{sid}".format(t = timeString, cid = newCust.custID, sid = availableServer.serverID)
            self.numServersBusy += 1
            self.numServersAvailable -= 1
        else:
            self.queue.put(newCust)
            print "  {t} Placing customer #{cid} to the ordering queue of size {size}".format(t = timeString, cid = newCust.custID, size = self.queue.qsize())
                
    def findAvailableServer(self):
        for server in self.servers:
            if not server.isBusy():
                return server
            
    def processQueue(self, availableServer, currentTime):
        timeString = currentTime.stringInfo()
        if self.queue.qsize() > 0:
            nextCust = self.queue.get()
            nextCust.queueTime = nextCust.arrivalTime.timeDiff(currentTime)
            hours = nextCust.queueTime/3600
            minutes = (nextCust.queueTime - 3600*hours)/60
            seconds = nextCust.queueTime - 3600*hours - 60*minutes
            if hours > 0:
                print "  {t} Assigning the next customer in line, customer #{cid}, to server #{sid} after spending {hr} hours, {minutes} minutes, and {sec} seconds in the queue. There are now {num} customers left in the queue.".format(t = timeString, cid = nextCust.custID, sid = availableServer.serverID, num = self.queue.qsize(), hr = hours, minutes = minutes, sec = seconds)
            elif minutes > 0:
                print "  {t} Assigning the next customer in line, customer #{cid}, to server #{sid} after spending {minutes} minutes, {sec} seconds in the queue. There are now {num} customers left in the queue.".format(t = timeString, cid = nextCust.custID, sid = availableServer.serverID, num = self.queue.qsize(), minutes = minutes, sec = seconds)
            else:
                print "  {t} Assigning the next customer in line, customer #{cid}, to server #{sid} after spending {sec} seconds in the queue. There are now {num} customers left in the queue.".format(t = timeString, cid = nextCust.custID, sid = availableServer.serverID, num = self.queue.qsize(), sec = seconds)
            self.numServersBusy += 1
            self.numServersAvailable -= 1
            availableServer.assignCustomer(nextCust, currentTime)
        else:
            print "  {t} There are no more customers in line, so server #{sid} is free right now.".format(t = timeString, sid = availableServer.serverID)
            
    def freeUpServers(self, currentTime):
        timeString = currentTime.stringInfo()
        for server in self.servers:
            if server.isBusy() and currentTime.compare(server.releaseTime) == 0:
                finishingCust = server.cust
                print "  {t} Customer #{cid} is done placing an order with server #{sid}".format(t = timeString, cid = finishingCust.custID, sid = server.serverID)
                self.numServersBusy -= 1
                self.numServersAvailable += 1
                server.releaseCustomer()
                self.processQueue(server, currentTime)
                finishingCust.setFoodDeliveryTime(currentTime)
                self.waitingForFood.append(finishingCust)
        for customer in self.waitingForFood:
            if currentTime.compare(customer.foodDeliveryTime) == 0:
                self.numCustomersServed += 1
                print "  {t} Customer #{cid} has received their food. {num} customers have been served food now.".format(t = timeString, cid = customer.custID, num = self.numCustomersServed)
                self.waitingForFood.remove(customer)
                
    def serverInfo(self):
        for server in self.servers:
            server.printInfo()
            