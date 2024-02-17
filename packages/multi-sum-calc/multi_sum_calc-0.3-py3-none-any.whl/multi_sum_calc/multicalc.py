def multi_calculator(a:float,b:float):
    '''this function takes two numeric values and multiplies them.'''
    try:
        product = a * b
        print(a, " * ", b, " = ", product)
        return product
    except:
        print("input needs to be numeric")
