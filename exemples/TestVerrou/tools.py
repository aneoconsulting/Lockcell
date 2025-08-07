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


def parseRes(tableau: list[list[str]]) -> list[list[str]]:
    return [
        [s.split("\t")[0] + ":" + s.split("\t")[1] for s in sous_liste] for sous_liste in tableau
    ]


def say(res, i):
    print(counter(i) + " results : " + parseRes(res).__str__() + "\n" + "-" * 80)


def say2(res):
    print("Found : " + parseRes(res).__str__() + "\n" + "-" * 80)


def finalSay(res, i):
    print(
        "\n"
        + "-" * 80
        + "\n"
        + "-" * 80
        + "\n"
        + "Recursions : "
        + i.__str__()
        + " | Total results : "
        + parseRes(res).__str__()
        + "\n"
        + "-" * 80
        + "\n"
        + "-" * 80
    )
