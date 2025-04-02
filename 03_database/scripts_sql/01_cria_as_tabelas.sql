-- Cria o Banco de Dados e as Tabelas conforme a modelagem no README.md

-- CREATE DATABASE sistema_operadoras;

CREATE TABLE enderecos (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(8) NOT NULL,
    logradouro VARCHAR(40),
    numero VARCHAR(20) NOT NULL,
    complemento VARCHAR(40),
    bairro VARCHAR(30) NOT NULL,
    cidade VARCHAR(30) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(8) NOT NULL
);

CREATE TABLE representantes (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(8),
    representante VARCHAR(50) NOT NULL,
    cargo_representante VARCHAR(40) NOT NULL
);

CREATE TABLE operadoras (
    registro_ans VARCHAR(8) PRIMARY KEY,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    razao_social VARCHAR(140) NOT NULL,
    nome_fantasia VARCHAR(140),
    modalidade VARCHAR(140),
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    regiao_de_comercializacao INT,
    data_registro_ans DATE NOT NULL,
    endereco_id INT UNIQUE,
    representante_id INT UNIQUE
);

CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans VARCHAR(8) NOT NULL,
    cd_conta_contabil INT NOT NULL,
    descricao TEXT NOT NULL,
    vl_saldo_inicial NUMERIC(15,2) NOT NULL,
    vl_saldo_final NUMERIC(15,2) NOT NULL
);

-- Adicionando as chaves estrangeiras
ALTER TABLE operadoras 
    ADD CONSTRAINT fk_endereco 
    FOREIGN KEY (endereco_id) REFERENCES enderecos(id);

ALTER TABLE operadoras 
    ADD CONSTRAINT fk_representante 
    FOREIGN KEY (representante_id) REFERENCES representantes(id);
