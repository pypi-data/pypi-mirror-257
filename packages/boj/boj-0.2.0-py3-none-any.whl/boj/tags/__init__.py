"""solved.ac에서 제공하는 acmicpc.net의 태그를 다루는 모듈.

사용법:
>>> import boj
>>> boj.tags.get(3)
"""

from .tag import Tag
from .database import __database__


def get(id: int) -> Tag:
    return __database__.get(str(id))


__all__ = [
    'Tag',
    'get',
]
