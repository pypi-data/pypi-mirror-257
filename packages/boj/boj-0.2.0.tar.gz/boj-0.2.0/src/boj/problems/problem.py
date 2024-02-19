from __future__ import annotations

import dataclasses
import logging
import typing

from boj.tags.tag import Tag
from boj.persistence import Entity


@dataclasses.dataclass(frozen=True)
class Problem(Entity):
    """solved.ac에서 제공하는 백준 문제 정보를 나타내는 클래스.

    다음과 같은 형식의 json 객체에 대한 mapping을 제공합니다. (예시는 "1000번 A+B" 문제)
    ```json
    {
        "problemId": 1000,
        "titleKo": "A+B",
        "titles": [
            {
                "language": "en",
                "languageDisplayName": "en",
                "title": "A+B",
                "isOriginal": true
            },
            {
                "language": "ko",
                "languageDisplayName": "ko",
                "title": "A+B",
                "isOriginal": true
            }
        ],
        "isSolvable": true,
        "isPartial": false,
        "acceptedUserCount": 279976,
        "level": 1,
        "votedUserCount": 203,
        "sprout": true,
        "givesNoRating": false,
        "isLevelLocked": true,
        "averageTries": 2.5397,
        "official": true,
        "tags": [
            {
                "key": "arithmetic",
                "isMeta": false,
                "bojTagId": 121,
                "problemCount": 1045,
                "displayNames": [
                    {
                        "language": "ko",
                        "name": "사칙연산",
                        "short": "사칙연산"
                    },
                    ...
                ],
                "aliases": [
                    { "alias": "덧셈" },
                    { "alias": "뺄셈" },
                    { "alias": "곱셈" },
                    ...
                ]
            },
            ...
        ],
        "metadata": {}
    }
    ```
    """

    @dataclasses.dataclass(frozen=True)
    class Title:
        language: str
        language_display_name: str
        title: str
        is_original: bool

    problem_id: int
    title_ko: str
    titles: typing.List[Title]
    is_solvable: bool
    is_partial: bool
    accepted_user_count: int
    level: int
    voted_user_count: int
    sprout: bool
    gives_no_rating: bool
    is_level_locked: bool
    average_tries: float
    official: bool
    tags: typing.List[Tag]
    metadata: typing.Dict

    def __getkey__(self) -> str:
        return self.problem_id.__str__()

    @classmethod
    def deserialize(cls, json: typing.Dict[str, typing.Any]) -> typing.Self:
        logging.debug(f'deserializing <Problem id={json["problemId"]}>')
        return Problem(
            problem_id=json["problemId"],
            title_ko=json["titleKo"],
            titles=[
                cls.Title(
                    language=title["language"],
                    language_display_name=title["languageDisplayName"],
                    title=title["title"],
                    is_original=title["isOriginal"],
                ) for title in json["titles"]
            ],
            is_solvable=json["isSolvable"],
            is_partial=json["isPartial"],
            accepted_user_count=json["acceptedUserCount"],
            level=json["level"],
            voted_user_count=json["votedUserCount"],
            sprout=json["sprout"],
            gives_no_rating=json["givesNoRating"],
            is_level_locked=json["isLevelLocked"],
            average_tries=json["averageTries"],
            official=json["official"],
            tags=[
                Tag.deserialize(tag) for tag in json["tags"]
            ],
            metadata={}
        )
