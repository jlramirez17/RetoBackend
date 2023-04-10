from pydantic import BaseModel


class NumbersSchema(BaseModel):
    numbers: list

class NumberSchema(BaseModel):
    number: int