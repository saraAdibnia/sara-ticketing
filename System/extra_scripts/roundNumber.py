import math


def to_point_five_up_round(n):
    floor = n - math.floor(n)
    if 0 < floor < 0.5:
        return math.floor(n) + 0.5
    elif floor == 0.5:
        return n
    
    return math.ceil(n)


def to_point_five_down_round(n):
    floor = n - math.floor(n)
    if floor > 0.5:
        return math.floor(n) + 0.5
    elif floor == 0.5:
        return n
    return math.floor(n)

"""
roundType : 0 , 1 , 2
"""


def findRoundKind(roundType=0, is_point_five=True):
    if is_point_five == False:
        if roundType == 0:
            kind = 0
        elif roundType == 1:
            kind = 2
    else:
        if roundType == 0:
            kind = 1
        elif roundType == 1:
            kind = 3
    if roundType == 2:
        kind = 4
    return kind


def rounding(kind=0, number=0):
    """[round numbers , we have 4 kind of Rounding numbers]

    Args:
        kind (int, optional): [ kind=0 :> round UP ,
                                kind=1 :> round UP pointFive,
                                kind=2 :> round DOWN,
                                kine=3 :> round DOWN pointFive]. Defaults to 0.
                                kind = 5 :> nor round
        number (int, optional): [number that want to rounding]. Defaults to 0.
    """
    rNum = 0
    if number > 0:
        if kind == 0:
            rNum = math.ceil(number)
        if kind == 1:
            rNum = to_point_five_up_round(number)
        if kind == 2:
            rNum = math.floor(number)
        if kind == 3:
            rNum = to_point_five_down_round(number)
    else:
        rNum = 0

    return rNum
