import Time
import arrivals
import printStatements as printFunc
import ServiceSystem
import inputs

end = Time.Time(days = inputs.days, hours = inputs.hours, minutes = inputs.minutes, seconds = inputs.seconds)

currentTime = Time.Time(seconds = 0)

serviceLines = ServiceSystem.ServiceSystem()

while currentTime.compare(end) <= 0:
    
    if currentTime.newHour():
        printFunc.printLine()
        incomingArrivals = arrivals.generateHourArrivals(currentTime)
        timePrint = currentTime.stringInfo()
        print "{timePrint}: {num} customers arriving this hour".format(timePrint = timePrint, num = len(incomingArrivals))
        printFunc.printLine()
    elif currentTime.newMinute():
        print "{timePrint}".format(timePrint = currentTime.stringInfo())
    
    serviceLines.freeUpServers(currentTime)
    serviceLines.recordQueueSize()
    
    for person in incomingArrivals:
        if currentTime.compare(person.arrivalTime) == 0:
            cTime = currentTime.stringInfo()
            print "  {cTime}: Customer #{custID} arrived at the restaurant".format(cTime = cTime, custID = person.custID)
            serviceLines.addCustomer(person, currentTime)
            incomingArrivals.remove(person)
            
    currentTime.addSecond()

serviceLines.printStatistics(currentTime)