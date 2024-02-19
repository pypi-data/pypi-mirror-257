import abc


class Entity(abc.ABC):
    @abc.abstractmethod
    def __getkey__(self) -> str:
        """`Database`에서 각 `Entity`를 구분하기 위한 고유 식별자를 반환합니다."""
        raise NotImplementedError
