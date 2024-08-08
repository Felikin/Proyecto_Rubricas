from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class Rubrica(BaseModel):
    nombre: str = Field(description="<Nombre de la rúbrica evaluada>")
    cumple: str = Field(description="<True o False dependiendo de si el docente cumple con la rúbrica>")
    observacion: str = Field(description="<Razón por la que crees que el docente cumple con la rúbrica>")


class Rubricas(BaseModel):
    rubricas: List[Rubrica] = Field(description="<Lista de rúbricas>")