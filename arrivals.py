import Customer
import Time
import random
import inputs

def generateHourArrivals(currentTime):
    arrivalRate = 3600.0/inputs.arrivalsPerHour
    currentSec = currentTime.totalSeconds()
    timeLeft = 3600
    secPassed = 0
    newCusts = []
    while secPassed < timeLeft:
        nextArrival = int(random.expovariate(1.0/arrivalRate))
        while nextArrival == 0:
            nextArrival = int(random.expovariate(1.0/arrivalRate))
        secPassed += nextArrival
        if secPassed < timeLeft:
            newCust = Customer.Customer(Time.Time(seconds = (currentSec + secPassed)))
            newCusts.append(newCust)
    return newCusts