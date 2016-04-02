import inputs
import Time
import Queue
import Server
import printStatements
import statistics
import random

class ServiceSystem(object):
    
    def __init__(self):
        self.numServers = int(inputs.numberOfServersAlwaysOpen) + int(inputs.numberOfAdditionalServersRushTime)
        self.numServersBusy = 0
        self.numServersAvailable = int(inputs.numberOfServersAlwaysOpen)
        self.numServersWorking = int(inputs.numberOfServersAlwaysOpen)
        self.numAdditionalServers = int(inputs.numberOfAdditionalServersRushTime)
        self.queue = Queue.Queue()
        self.servers = []
        self.initializeServers()
        self.numCustomersServed = 0
        self.waitingForFood = []
        self.queueTimes = []
        self.systemTimes = []
        self.numInQueueCumulative = 0
        self.currentlyRushTime = False
        self.revenues = 0.0
        self.foodCosts = 0.0
        
    def addRevenue(self):
        orderPrice = random.normalvariate(inputs.averageOrderPrice, inputs.orderSD)
        while orderPrice <= 0:
            orderPrice = random.normalvariate(inputs.averageOrderPrice, inputs.orderSD)
        self.revenues += orderPrice
        self.foodCosts += orderPrice * (inputs.foodCostPercent/100.0)
        
    def initializeServers(self):
        for i in range(0, self.numServersAvailable):
            newServer = Server.Server()
            self.servers.append(newServer)
        for i in range(0, self.numAdditionalServers):
            newServer = Server.Server()
            newServer.rushHour = True
            self.servers.append(newServer)
            
    def recordQueueSize(self):
        self.numInQueueCumulative += self.queue.qsize()
        
    def startRushTime(self, currentTime):
        if self.numAdditionalServers == 0:
            return
        timeString = currentTime.stringInfo()
        self.currentlyRushTime = True
        for server in self.servers:
            if server.rushHour:
                print "  {t} Opening server #{sid} for the rush".format(t = timeString, sid = server.serverID)
                server.lastOpenTime = Time.Time(currentTime)
                self.processQueue(server, currentTime)
        
    def endRushTime(self, currentTime):
        if self.numAdditionalServers == 0:
            return
        self.currentlyRushTime = False
        timeString = currentTime.stringInfo()
        printStatements.printStars()
        print "  {t} The rush time is ending now.".format(t = timeString)
        print "  All rush time servers (#{start} - #{end}) will process their final customers".format(start = int(inputs.numberOfServersAlwaysOpen) + 1, end = self.numServers)
        for server in self.servers:
            if server.rushHour:
                if not server.isBusy():
                    print "  Server #{sid} is currently not taking an order and will now close".format(sid = server.serverID)
                    server.close(currentTime)
                else:
                    print "  Server #{sid} is currently taking customer #{cid}'s order and will close after finishing up with the customer".format(sid = server.serverID, cid = server.cust.custID)
        printStatements.printStars()
        
    def addCustomer(self, newCust, currentTime):
        timeString = currentTime.stringInfo()
        availableServer = self.findAvailableServer()
        if availableServer is not None:
            self.queueTimes.append(0)
            availableServer.assignCustomer(newCust, currentTime)
            print "  {t} Assigning customer #{cid} to server #{sid}".format(t = timeString, cid = newCust.custID, sid = availableServer.serverID)
        else:
            self.queue.put(newCust)
            print "  {t} Placing customer #{cid} to the ordering queue of size {size}".format(t = timeString, cid = newCust.custID, size = self.queue.qsize())
            queueCutoff = inputs.queueCutoff
            if self.numAdditionalServers > 0 and not self.currentlyRushTime and self.queue.qsize() == queueCutoff:
                printStatements.printStars()
                print "  {t} Rush time has started.".format(t = timeString)
                print "  {t} Queue size is now {cutoff}. Opening an additional {num} counters".format(t = timeString, cutoff = queueCutoff, num = self.numAdditionalServers)
                printStatements.printStars()
                self.startRushTime(currentTime)
                
    def findAvailableServer(self):
        if self.numServersBusy >= self.numServersWorking:
            return None
        for server in self.servers:
            if not server.isBusy():
                if (server.rushHour and self.currentlyRushTime) or not server.rushHour:
                    return server
            
    def processQueue(self, availableServer, currentTime):
        timeString = currentTime.stringInfo()
        if self.queue.qsize() > 0:
            nextCust = self.queue.get()
            self.queueTimes.append(nextCust.arrivalTime.timeDiff(currentTime))
            nextCust.queueTime = nextCust.arrivalTime.timeDiff(currentTime)
            hours, minutes, seconds = Time.Time().breakdown(nextCust.queueTime)
            if hours > 0:
                print "  {t} Assigning the next customer in line, customer #{cid}, to server #{sid} after spending {hr} hours, {minutes} minutes, and {sec} seconds in the queue. There are now {num} customers left in the queue.".format(t = timeString, cid = nextCust.custID, sid = availableServer.serverID, num = self.queue.qsize(), hr = hours, minutes = minutes, sec = seconds)
            elif minutes > 0:
                print "  {t} Assigning the next customer in line, customer #{cid}, to server #{sid} after spending {minutes} minutes, {sec} seconds in the queue. There are now {num} customers left in the queue.".format(t = timeString, cid = nextCust.custID, sid = availableServer.serverID, num = self.queue.qsize(), minutes = minutes, sec = seconds)
            else:
                print "  {t} Assigning the next customer in line, customer #{cid}, to server #{sid} after spending {sec} seconds in the queue. There are now {num} customers left in the queue.".format(t = timeString, cid = nextCust.custID, sid = availableServer.serverID, num = self.queue.qsize(), sec = seconds)
            availableServer.assignCustomer(nextCust, currentTime)
        else:
            print "  {t} There are no more customers in line, so server #{sid} is free right now.".format(t = timeString, sid = availableServer.serverID)
            if self.currentlyRushTime:
                self.endRushTime(currentTime)
                availableServer.close(currentTime)
            
    def freeUpServers(self, currentTime):
        timeString = currentTime.stringInfo()
        for server in self.servers:
            if server.isBusy() and currentTime.compare(server.releaseTime) == 0:
                finishingCust = server.cust
                print "  {t} Customer #{cid} is done placing an order with server #{sid}".format(t = timeString, cid = finishingCust.custID, sid = server.serverID)
                self.addRevenue()
                server.releaseCustomer()
                if not server.rushHour or (server.rushHour and self.currentlyRushTime):
                    self.processQueue(server, currentTime)
                else:
                    print "  {t} It's past the rush hour, so server #{sid} is not taking any more customers".format(t = timeString, sid = server.serverID)
                    server.close(currentTime)
                finishingCust.setFoodDeliveryTime(currentTime)
                self.waitingForFood.append(finishingCust)
        for customer in self.waitingForFood:
            if currentTime.compare(customer.foodDeliveryTime) == 0:
                self.numCustomersServed += 1
                print "  {t} Customer #{cid} has received their food. {num} customers have been served food now.".format(t = timeString, cid = customer.custID, num = self.numCustomersServed)
                self.waitingForFood.remove(customer)
                self.systemTimes.append(customer.arrivalTime.timeDiff(currentTime))
                
    def serverInfo(self):
        for server in self.servers:
            server.printInfo()
            
    def serversOccupiedTotal(self):
        numOccupied = 0
        numTotal = 0
        for server in self.servers:
            if server.isBusy():
                numOccupied += 1
                #print "Server #{sid} counts in occupied".format(sid = server.serverID)
            if not server.rushHour or (server.rushHour and server.isBusy()):
                numTotal += 1
        return numOccupied, numTotal
    
    def getTotalServerUtilization(self, currentTime):
        sum = 0.0
        for server in self.servers:
            sum += server.getUtilizationTime(currentTime)
        return sum
    
    def getTotalServerOpenTime(self, currentTime):
        sum = 0.0
        for server in self.servers:
            sum += server.getOpenTime(currentTime)
        return sum
            
    def printStatistics(self, currentTime):
        printStatements.printStars()
        print "SIMULATION STATISTICS"
        printStatements.printStars()
        print "Number of customers served: {num}".format(num = self.numCustomersServed)
        numOccupied, numTotal = self.serversOccupiedTotal()
        print "Servers currently occupied: {num}/{total}".format(num = numOccupied, total = numTotal)
        serverUtilizationTime = self.getTotalServerUtilization(currentTime)
        serverOpenTime = self.getTotalServerOpenTime(currentTime)
        print "Average server utilization: {0:.2f}%".format(100.0*serverUtilizationTime/serverOpenTime)
        serverPay = (serverOpenTime/3600.0)*inputs.serverHourlyPay
        
        print ""
        
        print "Server pay: {0:.2f}".format(serverPay)
        print "Revenues: {0:.2f}".format(self.revenues)
        print "Food costs: {0:.2f}".format(self.foodCosts)
        meanQueueTime = int(statistics.mean(self.queueTimes))
        meanSystemTime = int(statistics.mean(self.systemTimes))
        mqHours, mqMinutes, mqSeconds = Time.Time().breakdown(meanQueueTime)
        msHours, msMinutes, msSeconds = Time.Time().breakdown(meanSystemTime)
        
        print ""
        print "Mean order queue time: {timeString}".format(timeString = Time.Time().printString(mqHours, mqMinutes, mqSeconds))
        print "Mean system time: {timeString}".format(timeString = Time.Time().printString(msHours, msMinutes, msSeconds))
        print "Average number of customers in the ordering queue: {0:.2f}".format(self.numInQueueCumulative/float(currentTime.totalSeconds()))
        printStatements.printStars()
            