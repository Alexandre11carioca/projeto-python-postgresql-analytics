CREATE TABLE IF NOT EXISTS incidentes (
  id                  INTEGER PRIMARY KEY,
  data_abertura       TIMESTAMP,
  data_fechamento     TIMESTAMP,
  sistema             TEXT,
  tipo_incidente      TEXT,
  prioridade          TEXT,
  status              TEXT,
  tempo_resolucao_min INTEGER,
  sla_min             INTEGER,
  sla_estourado       INTEGER,
  time_responsavel    TEXT,
  canal_deteccao      TEXT,
  impacto             INTEGER
);

CREATE INDEX IF NOT EXISTS idx_incidentes_data_abertura ON incidentes (data_abertura);
CREATE INDEX IF NOT EXISTS idx_incidentes_sistema ON incidentes (sistema);
CREATE INDEX IF NOT EXISTS idx_incidentes_prioridade ON incidentes (prioridade);
