import math

def mean(array):
    sum = 0.0
    for elem in array:
        sum += elem
    if len(array) > 0:
        return sum/len(array)
    else:
        return 0
    
#Allow mean to be passed in if already calculated before
def variance(array, avg = None):
    sum = 0.0
    if avg is None:
        avg = mean(array)
    else:
        avg = avg
    for elem in array:
        sum += pow(elem - avg, 2)
    if len(array) > 0:
        return sum/(len(array) - 1.0)
    else:
        return 0
    
#Allow mean to be passed in if already calculated before
def sd(array, avg = None):
    if avg is None:
        return pow(variance(array), 0.5)
    else:
        return pow(variance(array, avg = avg), 0.5)

def confidenceInterval(array):
    average = mean(array)
    var = variance(array, avg = average)
    root = pow( (var/float(len(array))), 0.5)
    zValue = 1.960 #95% confidence
    return average - zValue*root, average + zValue*root

def halfLength(array):
    average = mean(array)
    var = variance(array, avg = average)
    root = pow( (var/float(len(array))), 0.5)
    zValue = 1.960 #95% confidence
    return zValue*root