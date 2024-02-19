import typing

import requests

from boj.tags.tag import Tag
from boj.persistence import Database
from boj.persistence.databases import FileDatabase


__database__: Database[Tag]
__database_version__ = 0


class TagDatabase(FileDatabase[Tag]):
    def fetch(self, key: typing.Optional[str] = None) -> None:
        url='https://solved.ac/api/v3/tag/list'
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0' }
        items = requests.get(url, headers=headers).json()['items']
        self.save(*map(Tag.deserialize, items))


__database__ = TagDatabase(name='tags_v%s' % __database_version__)
