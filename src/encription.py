import random
SECURITY_LEVEL = 10
CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`~+={[}]|":;?/>.<,'

def incode(input_string: str):
    input_string += " "
    result = ""
    for char in input_string:
        for i in range(10):
            result += random.choice(CHARSET)
        result += char

    return result

def decode(input_string: str):
    result = ""
    for i in range(len(input_string) // 11):
        result += input_string[(11 * i) - 1]
    return result

sus = incode("sdrogoorientale")