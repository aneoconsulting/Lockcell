def counter(n: int):
    if n < 0:
        return "Number Err"
    if n <= 3:
        if n == 1:
            return "First"
        if n == 2:
            return "Second"
        if n == 3:
            return "Third"
    return n.__str__() + "th"


def RDDMin_print(res, i):
    print(counter(i) + " results : " + res.__str__() + "\n" + "-" * 80)


def SRDDMin_print(res):
    print("Found : " + res.__str__() + "\n" + "-" * 80)


def final_print(res, i):
    print(
        "\n"
        + "-" * 80
        + "\n"
        + "-" * 80
        + "\n"
        + "Recursions : "
        + i.__str__()
        + " | Total results : "
        + res.__str__()
        + "\n"
        + "-" * 80
        + "\n"
        + "-" * 80
    )
