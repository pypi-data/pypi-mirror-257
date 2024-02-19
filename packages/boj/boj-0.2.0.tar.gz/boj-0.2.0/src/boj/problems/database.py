import typing

import requests

from boj.problems.problem import Problem
from boj.persistence import Database
from boj.persistence.databases import FileDatabase


__database__: Database[Problem]
__database_version__ = 0


class ProblemDatabase(FileDatabase[Problem]):
    def fetch(self, key: typing.Optional[str] = None) -> None:
        assert key is not None
        url = 'https://solved.ac/api/v3/search/problem?query=%s' % key
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0' }
        items = requests.get(url, headers=headers).json()['items']
        self.save(*map(Problem.deserialize, items))


__database__ = ProblemDatabase(name='problems_v%s' % __database_version__)
