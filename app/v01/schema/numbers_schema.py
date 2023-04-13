from pydantic import BaseModel


class NumbersSchema(BaseModel):
    numbers: list[int]

class NumberSchema(BaseModel):
    number: int