from typing import Annotated

from pydantic import BaseModel, BeforeValidator, field_validator

LaxStr = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, int) else v),
]


class RegionsParams(BaseModel):
    """
    Attributes:
        nom:
        code:
        limit:
    """

    nom: str | None = None
    code: LaxStr | None = None
    limit: int | None = None


class RegionCodeParams(BaseModel):
    """
    Attributes:
        code:
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


class RegionsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        _score:
    """

    nom: str
    code: int
    _score: float | None = None
