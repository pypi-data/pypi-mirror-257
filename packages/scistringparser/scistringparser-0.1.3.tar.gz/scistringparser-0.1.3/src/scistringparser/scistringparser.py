
def parse_str(number_string: str) -> float:

    """
    Takes a string that contains a number with a metric prefix and
    converts it to a float.
    Examples: 1u -> 1e-6
            1.2k -> 1.2e3
    """

    prefix = {
    "q":pow(10, -30), #quecto
    "r":pow(10, -27), #ronto
    "y":pow(10, -24), #tocto
    "z":pow(10, -21), #zepto
    "a":pow(10, -18), #atto
    "f":pow(10, -15), #femto
    "p":pow(10, -12), #pico
    "n":pow(10, -9), #nano
    "u":pow(10, -6), #micro
    "m":pow(10, -3), #mili
    "c":pow(10, -2), #centi
    "d":pow(10, -1), #deci
    "da":pow(10, 1), #deca
    "h":pow(10, 2), #hecto
    "k":pow(10, 3), #quilo
    "M":pow(10, 6), #mega
    "G":pow(10, 9), #giga
    "T":pow(10, 12), #tera
    "P":pow(10, 15), #peta
    "E":pow(10, 18), #exa
    "Z":pow(10, 21), #zetta
    "Y":pow(10, 24), #yotta
    "R":pow(10, 27), #ronna
    "Q":pow(10, 30), #quetta
    }

    try:
        number = float(number_string[:-1])
        str_prefix = number_string[-1]
        number_prefix = prefix[str_prefix]
    
        result = number*number_prefix
        return result
    
    except TypeError:
        print("The value inserted is not a string!")

    except ValueError:
        print("The value inserted is not formatted correclty!")