import requests

from ..cache import session
from .schemas import (
    CommuneCodeParams,
    CommunesParams,
    DepartmentCommuneCodeParams,
    EpcisCodeParams,
)


class Api:
    """This is the api to interact with the Commune API

    Documentation : https://geo.api.gouv.fr/decoupage-administratif/communes

    """

    def __init__(self, **kwargs):
        self.url = kwargs.pop("url", "https://geo.api.gouv.fr")
        self.timeout = kwargs.get("timeout", 10)

    def communes(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (CommunesParams):
        """
        params = CommunesParams(**kwargs)
        return session.get(
            self.url + "/communes", params=params.model_dump(), timeout=self.timeout
        )

    def communes_by_code(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (CommuneCodeParams):
        """
        params = CommuneCodeParams(**kwargs)
        return session.get(
            self.url + "/communes/" + params.code,
            params=params.model_dump(),
            timeout=self.timeout,
        )

    def communes_by_epcis(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (EpcisCodeParams):
        """
        params = EpcisCodeParams(**kwargs)
        return session.get(
            self.url + f"/epcis/{params.code}/communes",
            params=params.model_dump(),
            timeout=self.timeout,
        )

    def communes_by_departement(self, **kwargs) -> requests.Response:
        """
        Parameters:
            **kwargs (DepartmentCommuneCodeParams):
        """
        params = DepartmentCommuneCodeParams(**kwargs)
        return session.get(
            self.url + f"/departements/{params.code}/communes",
            params=params.model_dump(),
            timeout=self.timeout,
        )
