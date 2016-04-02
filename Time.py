daySeconds = 60*60*24
hourSeconds = 60*60

class Time(object):
    
    def __init__(self, timeObject = None, seconds = 0, minutes = 0, hours = 0, days = 0):
        if timeObject is not None:
            self.days, self.hours, self.minutes, self.seconds = timeObject.getAttributes()
            self.hrFormat = (11 + self.hours % 12) + 1
        elif minutes == 0 and hours == 0 and days == 0:
            self.days = seconds/daySeconds
            seconds = seconds % daySeconds
            self.hours = seconds/3600
            self.hrFormat = (11 + self.hours)%12 + 1
            self.minutes = (seconds-3600*self.hours)/60
            self.seconds = (seconds-3600*self.hours - 60*self.minutes)
        else:
            self.days = days
            self.hours = hours
            self.hrFormat = (11 + self.hours)%12 + 1
            self.minutes = minutes
            self.seconds = seconds
            
    #If timeObject is greater, return -1
    #If timeObject less than, return 1
    #Else return 0
    def compare(self, timeObject):
        
        if self.days < timeObject.days:
            return -1
        elif self.days > timeObject.days:
            return 1
        
        if self.hours < timeObject.hours:
            return -1
        elif self.hours > timeObject.hours:
            return 1
        
        if self.minutes < timeObject.minutes:
            return -1
        elif self.minutes > timeObject.minutes:
            return 1
        
        if self.seconds < timeObject.seconds:
            return -1
        elif self.seconds > timeObject.seconds:
            return 1
        
        return 0
        
    def getDay(self):
        return self.days
    
    def totalSeconds(self):
        return (daySeconds*self.days + hourSeconds*self.hours + 60*self.minutes + self.seconds)
    
    #Not for printing use
    def getAttributes(self):
        return self.days, self.hours, self.minutes, self.seconds
    
    def getInfo(self):
        if self.hours > 11:
            amPm = "P.M."
        else:
            amPm = "A.M."
        return self.days, self.hours, self.minutes, self.seconds, amPm
    
    def getPrintInfo(self):
        if self.hours > 11:
            amPm = "P.M."
        else:
            amPm = "A.M."
        if self.hrFormat < 10:
            hrPrint = "0" + str(self.hrFormat)
        else:
            hrPrint = self.hrFormat
        if self.minutes < 10:
            minPrint = "0" + str(self.minutes)
        else:
            minPrint = self.minutes
        if self.seconds < 10:
            secPrint = "0" + str(self.seconds)
        else:
            secPrint = self.seconds
        return self.days, hrPrint, minPrint, secPrint, amPm
    
    def printInfo(self):
        day, hr, minutes, sec, amPm = self.getPrintInfo()
        print "{hr}:{minutes}:{sec} {amPm} (day #{day})".format(hr = hr, minutes = minutes, sec = sec, day = day+1, amPm = amPm)
        
    def stringInfo(self):
        day, hr, minutes, sec, amPm = self.getPrintInfo()
        return "{hr}:{minutes}:{sec} {amPm} (day #{day})".format(hr = hr, minutes = minutes, sec = sec, day = day+1, amPm = amPm)
        
    def printDebugInfo(self):
        print "Self.days = ", self.days
        print "Self.hours = ", self.hours
        print "Self.hrFormat = ", self.hrFormat
        print "Self.minutes = ", self.minutes
        print "Self.seconds = ", self.seconds
        
    def newHour(self):
        return self.minutes == 0 and self.seconds == 0
    
    def newMinute(self):
        return self.seconds == 0
    
    def incrementDay(self):
        self.days += 1
        
    def timeDiff(self, timeLater):
        return timeLater.totalSeconds() - self.totalSeconds()
        
    def addSeconds(self, numSeconds):
        seconds = self.totalSeconds() + numSeconds
        self.days = seconds/daySeconds
        seconds = seconds % daySeconds
        self.hours = seconds/3600
        self.hrFormat = (11 + self.hours)%12 + 1
        self.minutes = (seconds-3600*self.hours)/60
        self.seconds = (seconds-3600*self.hours - 60*self.minutes)
    
    def addSecond(self):
        self.seconds += 1
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
            if self.minutes == 60:
                self.hours += 1
                self.hrFormat = (11 + self.hours)%12 + 1
                self.minutes = 0
                if self.hours == 24:
                    self.days += 1
                    self.hours = 0
    