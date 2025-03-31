from pydantic import BaseModel, Field
from datetime import date


class OperatorRequest(BaseModel):
    registro_ans: str = Field(alias="Registro_ANS")
    cnpj: str = Field(alias="CNPJ")
    razao_social: str = Field(alias="Razao_Social")
    nome_fantasia: str | None = Field(default=None, alias="Nome_Fantasia")
    modalidade: str | None = Field(default=None, alias="Modalidade")
    logradouro: str | None = Field(default=None, alias="Logradouro")
    numero: str = Field(alias="Numero")
    complemento: str | None = Field(default=None, alias="Complemento")
    bairro: str = Field(alias="Bairro")
    cidade: str = Field(alias="Cidade")
    uf: str = Field(alias="UF")
    cep: str = Field(alias="CEP")
    ddd: str | None = Field(default=None, alias="DDD")
    telefone: str | None = Field(default=None, alias="Telefone")
    fax: str | None = Field(default=None, alias="Fax")
    endereco_eletronico: str | None = Field(
        default=None,
        alias="Endereco_eletronico"
    )
    representante: str = Field(alias="Representante")
    cargo_representante: str = Field(alias="Cargo_Representante")
    regiao_de_comercializacao: str | None = Field(
        default=None,
        alias="Regiao_de_Comercializacao"
    )
    data_registro_ans: date | None = Field(
        default=None,
        alias="Data_Registro_ANS"
    )
