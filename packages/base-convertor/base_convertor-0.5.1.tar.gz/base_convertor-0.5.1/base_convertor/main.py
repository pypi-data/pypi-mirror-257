def convert_base(number:str,input_base:int, output_base:int):
    """
    Converts a number from one base to another.

    Parameters:
        number (str): The number to be converted.
        input_base (int): The base of the input number. Must be between 2 and 36.
        output_base (int): The base to which the number is to be converted. Must be between 2 and 36.

    Returns:
        str: The converted number.
    """


    output = int(number, input_base)
    base_helper = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    quotient = int(output)
    remainder = ""
    while quotient > 0:
        basevalue = quotient % output_base
        if basevalue > 9:
            basevalue = base_helper[basevalue-10]
        remainder = remainder + str(basevalue)
        quotient //= output_base
    output = remainder[::-1]
    return output.upper()

creds = {
    "author": "IAMAJAYPRO",
    "ffc_profile": "https://bit.ly/ffc_iamajaypro"
}