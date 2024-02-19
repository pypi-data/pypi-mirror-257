from typing import Annotated

from pydantic import BaseModel, BeforeValidator, field_validator

LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class DepartmentsParams(BaseModel):
    """
    Attributes:
        nom:
        codeRegion:
        code:
        limit:
        fields:

    """

    nom: str | None = None
    codeRegion: LaxStr | None = None
    code: LaxStr | None = None
    limit: int | None = None
    fields: list[str] | None = None

    @field_validator("code")
    @classmethod
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v

    @field_validator("codeRegion")
    @classmethod
    def code_region_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class DepartmentCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
    """

    code: LaxStr | None = None
    fields: list | None = None
    limit: int | None = None

    @field_validator("code")
    @classmethod
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class RegionDepartmentCodeParams(BaseModel):
    """
    Attributes:
        regioncode:
        limit:
    """

    code: LaxStr | None = None
    limit: int | None = None

    @field_validator("code")
    @classmethod
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class DepartmentsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codeRegion: int
        fields:
        _score:
    """

    nom: str
    code: int
    codeRegion: int
    fields: list | None = None
    _score: float | None = None
