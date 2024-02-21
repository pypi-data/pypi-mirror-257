# type: ignore
from p52 import map  # it comes from utils.p52


def subdivide(start, end, n):
    return [map(i, 0, n - 1, start, end) for i in range(n)]


def widthRange(buffer=0):
    return (-width / 2 + buffer, width / 2 - buffer)


def heightRange(buffer=0):
    return (-height / 2 + buffer, height / 2 - buffer)


def randomPoint(buffer=0):
    return random(*widthRange(buffer)), random(*heightRange(buffer))
