def mean(array):
    sum = 0.0
    for elem in array:
        sum += elem
    if len(array) > 0:
        return sum/len(array)
    else:
        return 0