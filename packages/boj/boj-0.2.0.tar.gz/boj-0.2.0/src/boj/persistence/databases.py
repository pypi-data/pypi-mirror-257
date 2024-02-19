import abc
import typing

from boj.persistence.entity import Entity


E = typing.TypeVar('E', bound=Entity)


class Database(typing.Generic[E], abc.ABC):
    def __iter__(self) -> typing.Iterator[E]:
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: str) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, value: E) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __delitem__(self, key: str) -> None:
        raise NotImplementedError

    def get(self, key: str) -> E:
        if not self.__contains__(key):
            self.fetch(key)
        return self.__getitem__(key)

    @abc.abstractmethod
    def fetch(self, key: typing.Optional[str] = None) -> None:
        """`key`에 대한 값을 데이터베이스에서 찾을 수 없을 때, 데이터를 취득하는 방법을 정의합니다."""
        raise NotImplementedError

    def find(self, filter: typing.Callable[[E], bool]) -> typing.Optional[E]:
        for entity in self.__iter__():
            if filter(entity):
                return entity
        return None

    def filter(self, filter: typing.Callable[[E], bool]) -> typing.Iterator[E]:
        for entity in self.__iter__():
            if filter(entity):
                yield entity

    def save(self, *values: E) -> None:
        for value in values:
            self.__setitem__(value.__getkey__(), value)

    def clear(self) -> None:
        """delete all items"""
        for key in self.__iter__():
            del self.__delitem__[key]


class FileDatabase(typing.Generic[E], Database[E]):
    """boj 모듈이 설치된 디렉토리 안에 파일 데이터베이스를 구축합니다.

    파일 명은 boj/cache/*.db(m) 의 패턴을 사용합니다.
    """

    import pathlib
    import shelve

    DEFAULT_DIRECTORY = pathlib.Path(__file__).parent.parent / 'cache'

    __iter__ = shelve.Shelf.__iter__
    __len__ = shelve.Shelf.__len__
    __contains__ = shelve.Shelf.__contains__
    __getitem__ = shelve.Shelf.__getitem__
    __setitem__ = shelve.Shelf.__setitem__
    __delitem__ = shelve.Shelf.__delitem__

    def __init__(self, name: str) -> None:
        import os
        import shelve
        self.fspath = self.__class__.DEFAULT_DIRECTORY / name
        self.shelf: shelve.Shelf[E]
        try:
            os.makedirs(self.fspath.parent, exist_ok=True)
            self.shelf = shelve.open(self.fspath.__str__(), writeback=True, flag='c')
        except Exception:
            self.shelf = shelve.open(self.fspath.__str__(), writeback=True, flag='n')
        finally:
            self.__backup__ = { method.__name__: method for method in (
                self.get,
                self.save,
                self.clear,
            )}
            self.__dict__.update(self.shelf.__dict__)
            self.__dict__.update(self.__backup__)


    def save(self, *values: E) -> None:
        super().save(*values)
        self.shelf.sync()

    def clear(self) -> None:
        self.shelf.sync()
