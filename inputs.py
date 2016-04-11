serviceTimeMeanMinutes = 1.5
foodTimeWaitMeanMinutes = 5.2
arrivalsPerHour = 60
numberOfServersAlwaysOpen = 2

#This program supports additional servers
#to help during the rush periods. 
#They help when the queue reaches a specified size 
#until the queue goes back to zero.
#Leaving this as 0 will turn off this feature.
numberOfAdditionalServersRushTime = 2
queueCutoff = 30 #size of queue before putting additional servers on

serverHourlyPay = 7.25
averageOrderPrice = 15
orderSD = 5

#Simulation time
days = 0
hours = 5
minutes = 30
seconds = 0