from typing import Optional
from pydantic import BaseModel

class Jokes(BaseModel):
    id: Optional[int]
    value: str

    class Config:
        orm_mode = True

class JokeUpdate(BaseModel):   
    id:int
    value: str    
   
    class Config:
        orm_mode=True

class JokeDelete(BaseModel):   
    id:int
         
    class Config:
        orm_mode=True        