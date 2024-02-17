def sum_calculator(a:float,b:float):
    '''this function takes two numeric values and returns the sum.'''
    try:
        sum = a + b
        print(a, " + ", b, " = ", sum)
        return sum
    except:
        print("input needs to be numeric")
