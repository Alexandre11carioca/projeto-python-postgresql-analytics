# Projeto — Data Analytics com Python + PostgreSQL

Projeto de portfólio focado em **SQL para exploração/validação** e **Python para EDA e storytelling**, usando **PostgreSQL** como camada de dados.

## Stack
- PostgreSQL (Docker)
- Python (Pandas, Matplotlib)
- SQLAlchemy + psycopg
- python-dotenv (variáveis de ambiente)

## O que este projeto demonstra
- Modelagem de tabela e índices
- Carga de dados (CSV → PostgreSQL)
- KPIs de performance (**MTTR**, **SLA**, volume, top sistemas)
- Visualizações e resumo executivo (`INSIGHTS.md`)

## Como rodar
1) Subir PostgreSQL:
```bash
docker compose up -d
```

2) Crie `.env` (opcional):
- copie `.env.example` para `.env`

3) Instalar libs:
```bash
pip install -r requirements.txt
```

4) Carregar dados:
```bash
python src/load_to_postgres.py
```

5) Rodar análise (gera gráficos + insights):
```bash
python src/eda_postgres.py
```

## Entregáveis
- `src/outputs/incidentes_por_mes.png`
- `src/outputs/top_sistemas.png`
- `src/outputs/mttr_por_sistema.png`
- `src/outputs/sla_por_prioridade.png`
- `src/outputs/INSIGHTS.md`

## Como usar no currículo
**Projeto Python + PostgreSQL (Data Analytics):** carga de dados em PostgreSQL, queries SQL para KPIs (MTTR/SLA) e EDA com Python (Pandas/Matplotlib), gerando insights executivos.
