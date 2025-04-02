-- Insere os dados nas tabelas abaixo
-- Foi utilizado PSQL Tool (Terminal) p/ inserir os dados

-- Tabela enderecos
\copy enderecos (registro_ans, logradouro, numero, complemento, bairro, cidade, uf, cep) FROM 'C:\github_projetos\python\testes_em_python\teste_em_python\03_database\files\enderecos.csv' DELIMITER ';' CSV HEADER ENCODING 'utf8'

-- Tabela representantes
\copy representantes (registro_ans, representante, cargo_representante) FROM 'C:/github_projetos/python/testes_em_python/teste_em_python/03_database/files/representantes.csv' DELIMITER ';' CSV HEADER ENCODING 'utf8'

-- Tabela operadoras
\copy operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, ddd, telefone, fax, endereco_eletronico, regiao_de_comercializacao, data_registro_ans) FROM 'C:\github_projetos\python\testes_em_python\teste_em_python\03_database\files\operadoras.csv' DELIMITER ';' CSV HEADER ENCODING 'utf8'

-- Tabela demonstracoes_contabeis
\copy demonstracoes_contabeis (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) FROM 'C:\github_projetos\python\testes_em_python\teste_em_python\03_database\files\demonstracoes_contabeis_consolidado.csv' DELIMITER ';' CSV HEADER ENCODING 'utf8'


-- Atualiza os campos endereco_id e representante_id da tabela operadoras
UPDATE operadoras o
SET endereco_id = e.id
FROM enderecos e
WHERE o.registro_ans = e.registro_ans;

UPDATE operadoras o
SET representante_id = r.id
FROM representantes r
WHERE o.registro_ans = r.registro_ans;