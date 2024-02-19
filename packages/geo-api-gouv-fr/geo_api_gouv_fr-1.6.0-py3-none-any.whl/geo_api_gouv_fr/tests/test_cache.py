import time
from unittest import TestCase

import requests

from .. import RegionApi

WAIT_TIME = 0.2


class TestRegion(TestCase):
    def setUp(self) -> None:
        self.api = RegionApi()
        return super().setUp()

    def test_regions(self) -> requests.Response:
        time.sleep(WAIT_TIME)

        r = self.api.regions(limit=5)
        assert not r.from_cache

        r = self.api.regions(limit=5)
        assert r.from_cache
