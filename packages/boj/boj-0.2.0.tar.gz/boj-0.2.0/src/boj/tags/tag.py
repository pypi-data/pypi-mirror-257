from __future__ import annotations

import dataclasses
import logging
import typing

from boj.persistence.entity import Entity


@dataclasses.dataclass(frozen=True)
class Tag(Entity):
    """solved.ac에서 백준 문제에 부여한 태그 정보를 나타내는 클래스.

    다음과 같은 형식의 json 객체에 대한 mapping을 제공합니다. (예시는 "다이나믹 프로그래밍" 태그)
    ```json
    {
        "key": "dp",
        "isMeta": false,
        "bojTagId": 25,
        "problemCount": 3756,
        "displayNames": [
            { "language": "ko", "name": "다이나믹 프로그래밍", "short": "다이나믹 프로그래밍" },
            { "language": "en", "name": "dynamic programming", "short": "dp" },
            { "language": "ja", "name": "動的計画法", "short": "dp" }
        ],
        "aliases": [
            { "alias": "동적계획법" },
            { "alias": "동적 계획법" },
            { "alias": "다이나믹프로그래밍" }
        ]
    }
    ```
    """

    @dataclasses.dataclass(frozen=True)
    class DisplayName:
        language: str
        name: str
        short: str

    @dataclasses.dataclass(frozen=True)
    class Alias:
        alias: str

    key: str
    """태그를 구분하기 위한 고유한 값"""

    is_meta: bool
    boj_tag_id: int
    problem_count: int
    display_names: typing.List[DisplayName] = dataclasses.field(default_factory=list)
    aliases:typing.List[Alias] = dataclasses.field(default_factory=list)

    def __getkey__(self) -> str:
        return self.boj_tag_id.__str__()

    @classmethod
    def deserialize(cls, json: typing.Dict[str, typing.Any]) -> typing.Self:
        logging.debug(f'deserializing <Tag key={json["key"]}>')
        return Tag(
            key=json["key"],
            is_meta=json["isMeta"],
            boj_tag_id=json["bojTagId"],
            problem_count=json["problemCount"],
            display_names=[
                cls.DisplayName(
                    language=display_name['language'],
                    name=display_name['name'],
                    short=display_name['short'],
                ) for display_name in json["displayNames"]
            ],
            aliases=[
                cls.Alias(
                    alias=alias['alias'],
                ) for alias in json["aliases"]
            ]
        )
