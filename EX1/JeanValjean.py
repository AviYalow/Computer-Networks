

def splitToDigits(myNum):
    digits=""
    for x in str(myNum):
        x+=","
        digits += x
    return digits[:-1]

def sumOfDigits(myNum):
    digits = [int(x) for x in str(myNum)]
    return sum(digits)

def main():
    myNum= int(input("Please enter a 5 digit number "))
    print("You entered the number: {}".format(myNum))
    print("The digits of this number are: " + splitToDigits(myNum))
    print("The sum of the digits is: {}".format(sumOfDigits(myNum)))

if __name__ == "__main__":
    main()
