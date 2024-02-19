"""solved.ac에서 제공하는 acmicpc.net의 문제를 다루는 모듈.

사용법:
>>> import boj
>>> boj.problems.get(1000) # A+B
"""

from .problem import Problem
from .database import __database__


def get(id: int) -> Problem:
    return __database__.get(str(id))


__all__ = [
    'Problem',
    'get',
]
