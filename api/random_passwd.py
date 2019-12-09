from random import randint



def RandomPassword():
    code = ''
    for i in range(2):
        code += str(chr(randint(97, 122)))
    for i in range(6):
        code += str(randint(1, 9))
    return code

