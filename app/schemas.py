from pydantic import BaseModel # Base para validação de dados
from datetime import datetime # Para formatar a data na resposta

# O que a API vai devolver para o usuário quando ele consultar um CEP
class CEPOut(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str
    data_consulta: datetime # Mostra quando esse dado entrou no nosso sistema

    class Config:
        from_attributes = True # Permite que o Pydantic leia dados direto do SQLAlchemy