from __future__ import annotations

import dataclasses
import typing

from boj.problems.problem import Problem
from boj.persistence import Entity


@dataclasses.dataclass
class Class(Entity):
    level: int
    problems: typing.List[Problem] = dataclasses.field(default_factory=list)

    def __getkey__(self) -> str:
        return self.level.__str__()
