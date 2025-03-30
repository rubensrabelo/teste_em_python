-- As 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre
SELECT
	op.razao_social,
	SUM(dc.vl_saldo_final) AS total_despesas
FROM demonstracoes_contabeis dc
INNER JOIN operadoras op ON op.registro_ans = dc.reg_ans
WHERE dc.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
	AND dc.data >= '2024-09-01'
	AND dc.data <= '2024-10-31'
GROUP BY op.razao_social
ORDER BY total_despesas DESC
LIMIT 10;

-- As 10 operadoras com maiores despesas nessa categoria no último ano
SELECT
	op.razao_social,
	SUM(dc.vl_saldo_final) AS total_despesas
FROM demonstracoes_contabeis dc
INNER JOIN operadoras op ON op.registro_ans = dc.reg_ans
WHERE dc.descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
	AND dc.data >= '2024-01-01'
	AND dc.data <= '2024-10-31'
GROUP BY op.razao_social
ORDER BY total_despesas DESC
LIMIT 10;