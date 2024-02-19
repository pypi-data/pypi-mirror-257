from enum import Enum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, field_validator

LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class GeoFormat(Enum):
    """
    Attributes:
        type:
        fields:
        format:
    """

    json = "json"
    geojson = "geojson"


class CommunesParams(BaseModel):
    """
    Attributes:
        codePostal:
        lon:
        lat:
        nom:
        boost:
        code:
        siren:
        codeEpci:
        codeDepartement:
        codeRegion:
        zone:
        type:
        fields:
        format:
        geometry:
        limit:

    """

    codePostal: LaxStr | None = None
    lon: float | None = None
    lat: float | None = None
    nom: str | None = None
    boost: str | None = None
    code: LaxStr | None = None
    siren: str | None = None
    codeEpci: LaxStr | None = None
    codeDepartement: LaxStr | None = None
    codeRegion: LaxStr | None = None
    zone: str | None = None
    type: str | None = None
    fields: list[str] | None = None
    format: GeoFormat | None = GeoFormat.json
    geometry: str | None = None
    limit: int | None = None

    @field_validator("codeDepartement")
    @classmethod
    def code_departement_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v

    @field_validator("codeRegion")
    @classmethod
    def code_region_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class CommuneCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
        format:
        geometry:
    """

    code: LaxStr | None = None
    fields: list[str] | None = None
    geometry: str | None = None
    format: GeoFormat | None = GeoFormat.json
    limit: int | None = None


class EpcisCodeParams(CommuneCodeParams):
    pass


class DepartmentCommuneCodeParams(CommuneCodeParams):
    pass


class GeoCoords(BaseModel):
    type: str
    coordinates: list


class CommunesResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codePostaux:
        codeEpci:
        codeDepartement:
        codeRegion:
        population:
        _score:
    """

    nom: str
    code: LaxStr
    codePostaux: list[LaxStr] | None = None
    codeEpci: str | None = None
    codeDepartement: LaxStr | None = None
    codeRegion: LaxStr | None = None
    population: int | None = None
    _score: float | None = None
    # fields center, mairie, contour
    center: GeoCoords | None = None
    mairie: GeoCoords | None = None
    contour: GeoCoords | None = None
