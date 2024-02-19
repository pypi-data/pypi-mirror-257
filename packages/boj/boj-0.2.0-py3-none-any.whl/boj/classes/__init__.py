"""solved.ac의 클래스를 다루는 모듈.

클래스 목록은 https://solved.ac/ko/class 에서 확인할 수 있다.

사용법:
>>> import boj
>>> boj.classes.get(1)
"""

from .class_ import Class
from .database import __database__


def get(id: int) -> Class:
    return __database__.get(str(id))


__all__ = [
    'Class',
    'get',
]
