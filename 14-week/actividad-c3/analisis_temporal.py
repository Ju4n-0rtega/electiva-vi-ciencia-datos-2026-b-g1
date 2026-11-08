"""
Actividad calificable · Corte 3 — Análisis temporal y visualización
Caso: demanda diaria de una materia prima (acero laminado) en una planta industrial.

El script:
  1. Genera (con semilla fija) los movimientos de inventario de 2024-01-01 a 2026-11-01 (datos sintéticos).
  2. Los agrega por día con SQL y arma la serie temporal.
  3. Agrega por semana y por mes con resample y calcula la media móvil.
  4. Mide tendencia y estacionalidad.
  5. Construye 2 visualizaciones (evolución y comparación).
  6. Optimiza una consulta SQL y mide la mejora (EXPLAIN QUERY PLAN + tiempos).
"""
import json, sqlite3, statistics, tempfile, time, os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = Path(".")
rng = np.random.default_rng(2026)

# ------------------------------------------------------------------
# 1. DATOS SINTÉTICOS: movimientos de inventario del acero laminado
# ------------------------------------------------------------------
dias = pd.date_range("2024-01-01", "2026-11-01", freq="D")           # 1.036 días = 148 semanas exactas
t = np.arange(len(dias))
tendencia = 600 * (1 + 0.12 * t / 365)                               # crece ~12 % al año
estacional_anual = 1 + 0.18 * np.sin(2 * np.pi * (dias.dayofyear - 240) / 365)   # pico hacia noviembre-diciembre
factor_semana = np.array([1.10, 1.10, 1.05, 1.05, 1.00, 0.60, 0.30])  # lun..dom
demanda_base = tendencia * estacional_anual * factor_semana[dias.dayofweek] * rng.normal(1, 0.06, len(dias))

n_mov = np.round(demanda_base / 2).astype(int)                       # nº de movimientos de salida por día
fechas = np.repeat(dias.values, n_mov)
sku = rng.choice(["ACE-01", "ACE-02", "ACE-03"], size=len(fechas), p=[0.5, 0.3, 0.2])
cantidad = rng.choice([1, 2, 3], size=len(fechas), p=[0.25, 0.50, 0.25])
salidas = pd.DataFrame({"fecha": pd.to_datetime(fechas).strftime("%Y-%m-%d"), "sku": sku,
                        "tipo": "salida", "cantidad": cantidad})
n_ent = int(len(salidas) * 0.08)                                     # entradas (reposiciones): no cuentan como demanda
entradas = pd.DataFrame({"fecha": rng.choice(pd.Series(dias).dt.strftime("%Y-%m-%d"), n_ent),
                         "sku": rng.choice(["ACE-01", "ACE-02", "ACE-03"], n_ent),
                         "tipo": "entrada", "cantidad": rng.choice([20, 40, 60], n_ent)})
movimientos = pd.concat([salidas, entradas], ignore_index=True)
print(f"Movimientos generados: {len(movimientos):,} filas ({len(salidas):,} salidas y {len(entradas):,} entradas)")

# ------------------------------------------------------------------
# 2. SQL → serie diaria (la base queda en un archivo temporal)
# ------------------------------------------------------------------
ruta_db = Path(tempfile.gettempdir()) / "movimientos_inventario.db"
if ruta_db.exists():
    ruta_db.unlink()
con = sqlite3.connect(ruta_db)
movimientos.to_sql("movimientos", con, index=False)

serie = pd.read_sql_query("""
    SELECT fecha, SUM(cantidad) AS unidades
    FROM movimientos
    WHERE tipo = 'salida'
    GROUP BY fecha
    ORDER BY fecha
""", con, parse_dates=["fecha"]).set_index("fecha")["unidades"]
serie = serie.asfreq("D")
assert serie.isna().sum() == 0 and len(serie) == len(dias)
serie.rename("unidades").to_csv(SALIDA / "serie_diaria.csv")

# ------------------------------------------------------------------
# 3. RESAMPLE + MEDIA MÓVIL
# ------------------------------------------------------------------
semanal = serie.resample("W-SUN").sum()                              # semanas lunes-domingo (todas completas)
media_movil = semanal.rolling(window=4).mean()                       # media móvil de 4 semanas
mensual = serie.resample("MS").sum()
mensual = mensual[mensual.index < "2026-11-01"]                      # noviembre de 2026 solo tiene 1 día: se excluye
pd.DataFrame({"unidades_semana": semanal, "media_movil_4s": media_movil.round(1)}).to_csv(SALIDA / "serie_semanal.csv")

# ------------------------------------------------------------------
# 4. TENDENCIA Y ESTACIONALIDAD
# ------------------------------------------------------------------
x = np.arange(len(semanal))
pendiente, intercepto = np.polyfit(x, semanal.values, 1)
primer_anio = semanal.iloc[:52].mean()
ultimo_anio = semanal.iloc[-52:].mean()
crec_total = 100 * (ultimo_anio / primer_anio - 1)

# Estacionalidad anual: solo con años completos (2024 y 2025). Cada mes se divide por el promedio de su propio año,
# así el crecimiento de largo plazo no se confunde con la estacionalidad.
completos = serie["2024":"2025"]
prom_dia_mes = completos.groupby([completos.index.year, completos.index.month]).mean()
rel_anio = prom_dia_mes / prom_dia_mes.groupby(level=0).transform("mean")
idx_mes = rel_anio.groupby(level=1).mean()
mes_pico, mes_valle = int(idx_mes.idxmax()), int(idx_mes.idxmin())

dow = serie.groupby(serie.index.dayofweek).mean()
lab_dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
ratio_domingo = dow.iloc[6] / dow.iloc[:5].mean()
ratio_sabado = dow.iloc[5] / dow.iloc[:5].mean()

m25 = mensual[mensual.index.year == 2025].iloc[:10]
m26 = mensual[mensual.index.year == 2026].iloc[:10]
crec_25_26 = 100 * (m26.sum() / m25.sum() - 1)

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# ------------------------------------------------------------------
# 5. DOS VISUALIZACIONES
# ------------------------------------------------------------------
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
AZUL, NARANJA, GRIS = "#1f77b4", "#d95f02", "#9aa0a6"

# 5.1 Evolución: línea semanal + media móvil
fig, ax = plt.subplots(figsize=(11, 5.6))
ax.plot(semanal.index, semanal.values, color=GRIS, linewidth=1.2, label="Demanda semanal")
ax.plot(media_movil.index, media_movil.values, color=AZUL, linewidth=2.8, label="Media móvil de 4 semanas")
ax.set_ylim(0, semanal.max() * 1.12)
ax.set_ylabel("Unidades por semana (eje desde 0)")
ax.set_xlabel("Semana (lunes a domingo)")
ax.set_title(f"La demanda semanal de acero creció {crec_total:.0f} % entre el primer y el último año\n"
             f"y se repite cada año: pico en {MESES[mes_pico-1].lower()}., valle en {MESES[mes_valle-1].lower()}.",
             loc="left", fontweight="bold")
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", alpha=0.25)
fig.text(0.01, 0.005, "Fuente: movimientos de salida del acero laminado, 2024-01-01 a 2026-11-01 (datos sintéticos). "
         "Semanas completas lunes-domingo.", fontsize=8, color="#555")
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(SALIDA / "evolucion.png", dpi=150)
plt.close(fig)

# 5.2 Comparación: barras agrupadas por mes, 2025 vs 2026 (enero a octubre)
anchos = 0.38
pos = np.arange(10)
fig, ax = plt.subplots(figsize=(11, 5.6))
b1 = ax.bar(pos - anchos / 2, m25.values / 1000, anchos, color=GRIS, label="2025")
b2 = ax.bar(pos + anchos / 2, m26.values / 1000, anchos, color=NARANJA, label="2026")
ax.set_xticks(pos)
ax.set_xticklabels(MESES[:10])
ax.set_ylim(0, max(m25.max(), m26.max()) / 1000 * 1.15)
ax.set_ylabel("Miles de unidades por mes (eje desde 0)")
ax.set_xlabel("Mes (enero a octubre; noviembre de 2026 aún no termina)")
ax.set_title(f"De enero a octubre, la demanda de 2026 supera a la de 2025 en {crec_25_26:.0f} %\n"
             f"y el mes más fuerte es {MESES[int(m26.values.argmax())].lower()}.",
             loc="left", fontweight="bold")
ax.bar_label(b2, fmt="%.0f", padding=2, fontsize=8, color=NARANJA)
ax.legend(frameon=False, loc="upper left", ncol=2)
ax.grid(axis="y", alpha=0.25)
fig.text(0.01, 0.005, "Fuente: movimientos de salida del acero laminado agregados por mes (datos sintéticos). "
         "Las barras parten de 0.", fontsize=8, color="#555")
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(SALIDA / "comparacion.png", dpi=150)
plt.close(fig)

# ------------------------------------------------------------------
# 6. OPTIMIZACIÓN SQL (mismo resultado, menos trabajo)
# ------------------------------------------------------------------
Q_ORIGINAL = """
SELECT fecha, SUM(cantidad) AS unidades
FROM movimientos
WHERE tipo = 'salida' AND strftime('%Y-%m', fecha) = '2026-03'
GROUP BY fecha
ORDER BY fecha
"""
Q_RANGO = """
SELECT fecha, SUM(cantidad) AS unidades
FROM movimientos
WHERE tipo = 'salida' AND fecha >= '2026-03-01' AND fecha < '2026-04-01'
GROUP BY fecha
ORDER BY fecha
"""
IDX = "CREATE INDEX idx_mov_tipo_fecha ON movimientos(tipo, fecha)"

def plan(q):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)]

def medir(q, veces=15):
    tiempos = []
    for _ in range(veces):
        t0 = time.perf_counter()
        filas = con.execute(q).fetchall()
        tiempos.append((time.perf_counter() - t0) * 1000)
    return statistics.median(tiempos), filas

con.execute("DROP INDEX IF EXISTS idx_mov_tipo_fecha")
plan_a = plan(Q_ORIGINAL); t_a, res_a = medir(Q_ORIGINAL)
plan_b = plan(Q_RANGO);    t_b, res_b = medir(Q_RANGO)
con.execute(IDX); con.commit()
plan_c = plan(Q_RANGO);    t_c, res_c = medir(Q_RANGO)
assert res_a == res_b == res_c, "Las tres consultas deben dar exactamente el mismo resultado"

resultados = {
    "filas_movimientos": int(len(movimientos)),
    "dias_serie": int(len(serie)), "semanas": int(len(semanal)),
    "pendiente_unid_por_semana": round(float(pendiente), 2),
    "media_semanal_primer_anio": round(float(primer_anio)), "media_semanal_ultimo_anio": round(float(ultimo_anio)),
    "crecimiento_primer_a_ultimo_anio_pct": round(float(crec_total), 1),
    "crecimiento_ene_oct_2026_vs_2025_pct": round(float(crec_25_26), 1),
    "unidades_ene_oct_2025": int(m25.sum()), "unidades_ene_oct_2026": int(m26.sum()),
    "mes_pico": MESES[mes_pico - 1], "indice_pico": round(float(idx_mes.max()), 2),
    "mes_valle": MESES[mes_valle - 1], "indice_valle": round(float(idx_mes.min()), 2),
    "ratio_sabado_vs_semana": round(float(ratio_sabado), 2), "ratio_domingo_vs_semana": round(float(ratio_domingo), 2),
    "demanda_media_diaria_por_dia": {lab_dias[i]: round(float(dow.iloc[i])) for i in range(7)},
    "mes_max_2026": MESES[int(m26.values.argmax())],
    "sql": {
        "filas_resultado": len(res_a),
        "original_ms": round(t_a, 2), "rango_ms": round(t_b, 2), "rango_indice_ms": round(t_c, 2),
        "mejora_total_x": round(t_a / t_c, 1), "mejora_solo_rango_x": round(t_a / t_b, 1),
        "plan_original": plan_a, "plan_rango": plan_b, "plan_rango_indice": plan_c,
    },
}
json.dump(resultados, open("resultados.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(resultados, ensure_ascii=False, indent=2))
con.close()
