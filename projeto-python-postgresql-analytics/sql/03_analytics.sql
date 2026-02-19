-- 1) Incidentes por mês
SELECT
  to_char(date_trunc('month', data_abertura), 'YYYY-MM') AS mes,
  COUNT(*) AS total
FROM incidentes
GROUP BY 1
ORDER BY 1;

-- 2) Top sistemas por volume
SELECT sistema, COUNT(*) AS total
FROM incidentes
GROUP BY 1
ORDER BY total DESC
LIMIT 10;

-- 3) MTTR por sistema (somente resolvidos)
SELECT sistema, ROUND(AVG(tempo_resolucao_min)::numeric, 2) AS mttr_min
FROM incidentes
WHERE status = 'Resolvido'
GROUP BY 1
ORDER BY mttr_min DESC;

-- 4) % SLA estourado por prioridade (somente resolvidos)
SELECT prioridade,
       ROUND((SUM(sla_estourado)::numeric / COUNT(*)) * 100, 2) AS pct_sla_estourado
FROM incidentes
WHERE status = 'Resolvido'
GROUP BY 1
ORDER BY prioridade;

-- 5) Picos de incidentes: dia da semana x hora
SELECT
  EXTRACT(DOW FROM data_abertura) AS dow,
  EXTRACT(HOUR FROM data_abertura) AS hora,
  COUNT(*) AS total
FROM incidentes
GROUP BY 1,2
ORDER BY 1,2;
