from pydantic import BaseModel, model_validator
from typing import Optional


class OABRequest(BaseModel):
    oab: Optional[str] = None
    name: Optional[str] = None
    uf: Optional[str] = None
    categoria: Optional[str] = None

    @model_validator(mode='before')
    def check_search_criteria(cls, values):
        oab = values.get('oab')
        name = values.get('name')
        
        if not (oab or (name and len(name) >= 3)):
            raise ValueError(
                'A busca requer que o número da inscrição OAB esteja presente ou que o nome tenha 3 ou mais caracteres.'
            )
        return values


class OABResponse(BaseModel):
    oab: str
    nome: str
    uf: str
    categoria: str
    situacao: str
    