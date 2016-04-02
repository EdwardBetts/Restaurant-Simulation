import Time
import arrivals
import printStatements as printFunc

end = Time.Time(days = 0, hours = 6)

currentTime = Time.Time(0)

while currentTime.compare(end) <= 0:
    if currentTime.newHour():
        printFunc.printLine()
        incomingArrivals = arrivals.generateHourArrivals(currentTime)
        timePrint = currentTime.stringInfo()
        print "{timePrint}: {num} customers arriving this hour".format(timePrint = timePrint, num = len(incomingArrivals))
        printFunc.printLine()
    if currentTime.newMinute():
        print "{timePrint}".format(timePrint = currentTime.stringInfo())
    currentTime.addSecond()
    
    for person in incomingArrivals:
        if currentTime.compare(person.arrivalTime) == 0:
            cTime = currentTime.stringInfo()
            print "  {cTime}: Customer #{custID} arrived at the restaurant".format(cTime = cTime, custID = person.custID)
            incomingArrivals.remove(person)