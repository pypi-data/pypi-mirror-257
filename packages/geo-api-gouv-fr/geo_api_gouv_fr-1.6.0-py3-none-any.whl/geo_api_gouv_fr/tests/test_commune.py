# from ..commune.schemas import Geometry, GpsCoordinate, AddressFeature
import time
from unittest import TestCase

import requests

from .. import CommuneApi, CommunesResponse

WAIT_TIME = 0.2


class TestCommune(TestCase):

    def setUp(self) -> None:
        self.api = CommuneApi()
        return super().setUp()

    def test_communes(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.communes(codePostal="44000", limit=5)
        self.assertTrue(r.status_code == 200)

        return r

    def test_communes_by_code(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes_by_code(code=44109)
        self.assertTrue(r.status_code == 200)

    def test_communes_by_departement(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes_by_departement(code="57")
        self.assertTrue(r.status_code == 200)

    def test_communes_by_epcis(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes_by_epcis(code="244400404")
        self.assertTrue(r.status_code == 200)

    def test_communes_response(self) -> None:
        results = [CommunesResponse(**r) for r in self.test_communes().json()]
        self.assertTrue(results is not None)

    def test_communes_geometry(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.communes(code="75056", fields=["centre"])
        self.assertTrue(r.status_code == 200)
        data = r.json()
        self.assertTrue("centre" in data[0])

        r = self.api.communes(code="75056", fields=["mairie"])
        self.assertTrue(r.status_code == 200)
        data = r.json()
        self.assertTrue("mairie" in data[0])

        r = self.api.communes(code="75056", fields=["contour"])
        self.assertTrue(r.status_code == 200)
        data = r.json()
        self.assertTrue("contour" in data[0])

        # response output
        r = self.api.communes(code="75056", fields=["contour", "center", "mairie"])
        self.assertTrue(r.status_code == 200)
        data = r.json()
        self.assertTrue("contour" in data[0])
        results = [CommunesResponse(**r) for r in data]
        self.assertTrue(results is not None)

        # commune by code
        r = self.api.communes_by_code(code="75056", fields=["centre"])
        self.assertTrue(r.status_code == 200)
        data = r.json()
        self.assertTrue("centre" in data)
