import pandas as pd

df = pd.read_csv("pedidos_materia_prima_limpio.csv", parse_dates=["fecha_pedido", "fecha_entrega_estimada"])

print("=" * 60)
print("Pregunta 1: ¿Qué proveedor tiene el mayor tiempo promedio de entrega (días)?")
print("=" * 60)
q1 = df.groupby("proveedor")["dias_entrega"].mean().round(1).sort_values(ascending=False)
print(q1)

print()
print("=" * 60)
print("Pregunta 2: ¿Cuál es la materia prima con mayor cantidad total pedida")
print("entre los pedidos ya 'Entregado'?")
print("=" * 60)
entregados = df[df["estado"] == "Entregado"]
q2 = entregados.groupby("materia_prima")["cantidad_pedida"].sum().round(1).sort_values(ascending=False)
print(q2)
