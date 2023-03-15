import types
from pydantic import BaseModel, validator


class Post(BaseModel):
    result: object
    errorMessage: types.NoneType
    localizationKey: types.NoneType
    arguments: types.NoneType
    hasError: bool

    @validator("hasError")
    def check_that_error_is_absent(cls, v):
        if v == True:
            raise ValueError('Error is not absent.')
        else:
            return v
