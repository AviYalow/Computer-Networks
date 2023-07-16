def splitToDigits(myNum):
    """
    Split the given number to digits separate by ','
     Args:
     myNum- the number given by the user
     Return value:
     the digits of the number separate by ','
     """
    digits = ""
    for x in str(myNum):
        x += ","
        digits += x
    return digits[:-1]


def sumOfDigits(myNum):
    """
    Sum the digits of the given number
     Args:
     myNum- the number given by the user
     Return value:
     the sum of the number digits
     """
    digits = [int(x) for x in str(myNum)]
    return sum(digits)


def isValidDigits(element):
    """
    Check if the given input are a five digits number
     Args:
     element- the input given by the user
     Return value:
     True if its five digits number otherwise False
     """
    if type(element) != int:
        return False
    elif len(str(element)) == NUM_OF_DIGITS and int(element) > 0:
        return True
    else:
        return False


def main():
    assert (isValidDigits(12345)) is True
    assert (isValidDigits("abcd")) is False
    assert (isValidDigits("12345")) is False
    assert (isValidDigits(00000)) is False
    assert (isValidDigits(123456)) is False
    assert (isValidDigits(123)) is False
    assert (isValidDigits(None)) is False

    validInput = False

    while not validInput:
        try:
            # get the number from the user and try to parse it to int type
            # if the parse didn't work,
            # exception will throw, we catch it and ask again for new input
            myNum = int(input("Please insert a 5 digit number "))

            # get here if the parse succeeded,
            # and now we check if it is a five digits number
            # if not, its ask again for new input
            validInput = isValidDigits(myNum)
        except ValueError:
            continue

    print("You entered the number: {}".format(myNum))
    print("The digits of this number are: " + splitToDigits(myNum))
    print("The sum of the digits is: {}".format(sumOfDigits(myNum)))


if __name__ == "__main__":
    # constant value
    NUM_OF_DIGITS = 5
    main()
