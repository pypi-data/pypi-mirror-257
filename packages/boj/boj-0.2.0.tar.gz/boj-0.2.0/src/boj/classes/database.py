import typing

import requests

from boj.classes.class_ import Class
from boj.problems.problem import Problem
from boj.persistence import Database
from boj.persistence.databases import FileDatabase


__database__: Database[Class]
__database_version__ = 0


class ClassDatabase(FileDatabase[Class]):
    def fetch(self, key: typing.Optional[str] = None) -> None:
        for level in range(1, 11):
            url = 'https://solved.ac/api/v3/search/problem?query=in_class:%d' % level
            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0' }
            items = requests.get(url, headers=headers).json()['items']
            self.save(Class(level=level, problems=list(map(Problem.deserialize, items))))


__database__ = ClassDatabase(name='classes_v%s' % __database_version__)
