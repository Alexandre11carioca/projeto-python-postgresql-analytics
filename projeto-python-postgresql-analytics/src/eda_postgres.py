from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL", "postgresql+psycopg://analytics:analytics@localhost:5432/analytics_db")

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

def q(engine, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, engine)

def main():
    engine = create_engine(DB_URL)

    by_month = q(engine, """
        SELECT to_char(date_trunc('month', data_abertura), 'YYYY-MM') AS mes,
               COUNT(*) AS total
        FROM incidentes
        GROUP BY 1
        ORDER BY 1;
    """)
    ax = by_month.set_index("mes")["total"].plot(kind="line")
    ax.set_title("Incidentes por mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Total")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "incidentes_por_mes.png", dpi=160)
    plt.close()

    top_sys = q(engine, """
        SELECT sistema, COUNT(*) AS total
        FROM incidentes
        GROUP BY 1
        ORDER BY total DESC
        LIMIT 8;
    """)
    ax = top_sys.set_index("sistema")["total"].plot(kind="bar")
    ax.set_title("Top sistemas por incidentes")
    ax.set_xlabel("Sistema")
    ax.set_ylabel("Total")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "top_sistemas.png", dpi=160)
    plt.close()

    mttr = q(engine, """
        SELECT sistema, AVG(tempo_resolucao_min) AS mttr_min
        FROM incidentes
        WHERE status = 'Resolvido'
        GROUP BY 1
        ORDER BY mttr_min DESC
        LIMIT 8;
    """)
    ax = mttr.set_index("sistema")["mttr_min"].plot(kind="bar")
    ax.set_title("MTTR médio por sistema (min)")
    ax.set_xlabel("Sistema")
    ax.set_ylabel("MTTR (min)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "mttr_por_sistema.png", dpi=160)
    plt.close()

    sla = q(engine, """
        SELECT prioridade,
               (SUM(sla_estourado)::numeric / COUNT(*)) * 100 AS pct_sla_estourado
        FROM incidentes
        WHERE status = 'Resolvido'
        GROUP BY 1
        ORDER BY prioridade;
    """)
    ax = sla.set_index("prioridade")["pct_sla_estourado"].plot(kind="bar")
    ax.set_title("% SLA estourado por prioridade")
    ax.set_xlabel("Prioridade")
    ax.set_ylabel("%")
    plt.tight_layout()
    plt.savefig(OUT / "sla_por_prioridade.png", dpi=160)
    plt.close()

    total = int(q(engine, "SELECT COUNT(*) AS n FROM incidentes;").iloc[0,0])
    top3 = top_sys.head(3).apply(lambda r: f"{r['sistema']} ({int(r['total'])})", axis=1).tolist()
    worst_mttr = mttr.head(3).apply(lambda r: f"{r['sistema']} ({r['mttr_min']:.1f} min)", axis=1).tolist()
    worst_sla = sla.sort_values("pct_sla_estourado", ascending=False).head(2).apply(
        lambda r: f"{r['prioridade']} ({r['pct_sla_estourado']:.1f}%)", axis=1
    ).tolist()

    insights = [
        f"- Total de registros analisados: {total}",
        f"- Top 3 sistemas por volume: {', '.join(top3)}",
        f"- Maior MTTR (Top 3): {', '.join(worst_mttr)}",
        f"- Prioridades com maior % SLA estourado: {', '.join(worst_sla)}",
    ]
    (OUT / "INSIGHTS.md").write_text("\n".join(insights), encoding="utf-8")
    print("OK: outputs gerados em", OUT)

if __name__ == "__main__":
    main()
