import pandas as pd
import numpy as np

df = pd.read_csv("pedidos_materia_prima.csv", dtype=str)

print("=" * 60)
print("ANTES DE LA LIMPIEZA")
print("=" * 60)
print(f"Filas totales: {len(df)}")
print(f"Filas duplicadas (exactas): {df.duplicated().sum()}")
print("\nValores nulos/vacíos por columna:")
nulos_antes = {}
for col in df.columns:
    vacios = df[col].isna().sum() + (df[col] == "").sum()
    nulos_antes[col] = vacios
    print(f"  {col}: {vacios}")
print("\nTipos de dato (todas como texto al cargar):")
print(df.dtypes)
print("\nValores únicos de 'proveedor' (antes de normalizar):")
print(sorted(df['proveedor'].unique()))
print("\nValores únicos de 'estado' (antes de normalizar):")
print(sorted(df['estado'].unique()))

# -------------------------------------------------------
# LIMPIEZA
# -------------------------------------------------------

# 1) Quitar duplicados exactos
df = df.drop_duplicates()

# 2) Normalizar texto: proveedor y estado a formato consistente (Title Case)
df['proveedor'] = df['proveedor'].str.strip().str.title()
df['estado'] = df['estado'].str.strip().str.title()

# 3) Limpiar cantidad_pedida: quitar unidades de texto y convertir a número
df['cantidad_pedida'] = (
    df['cantidad_pedida']
    .str.replace(r'[a-zA-Záéíóú]+', '', regex=True)
    .str.strip()
)
df['cantidad_pedida'] = pd.to_numeric(df['cantidad_pedida'], errors='coerce')

# 4) Normalizar fechas (varios formatos) a un único formato datetime
def parse_fecha(x):
    if pd.isna(x) or x == "":
        return pd.NaT
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"):
        try:
            return pd.to_datetime(x, format=fmt)
        except ValueError:
            continue
    return pd.NaT

df['fecha_pedido'] = df['fecha_pedido'].apply(parse_fecha)
df['fecha_entrega_estimada'] = df['fecha_entrega_estimada'].apply(parse_fecha)

# 5) Tratamiento de nulos:
#    - cantidad_pedida nula: es un dato crítico para el análisis de inventario -> se elimina la fila
filas_antes_drop = len(df)
df = df.dropna(subset=['cantidad_pedida'])
filas_eliminadas_cantidad = filas_antes_drop - len(df)

#    - fecha_entrega_estimada nula: se imputa con la mediana de tiempo de entrega (en días) de ese mismo proveedor
df['dias_entrega'] = (df['fecha_entrega_estimada'] - df['fecha_pedido']).dt.days
mediana_dias_por_proveedor = df.groupby('proveedor')['dias_entrega'].median()

def imputar_fecha_entrega(row):
    if pd.isna(row['fecha_entrega_estimada']) and not pd.isna(row['fecha_pedido']):
        mediana = mediana_dias_por_proveedor.get(row['proveedor'], np.nan)
        if not pd.isna(mediana):
            return row['fecha_pedido'] + pd.Timedelta(days=mediana)
    return row['fecha_entrega_estimada']

n_imputadas = df['fecha_entrega_estimada'].isna().sum()
df['fecha_entrega_estimada'] = df.apply(imputar_fecha_entrega, axis=1)
df['dias_entrega'] = (df['fecha_entrega_estimada'] - df['fecha_pedido']).dt.days

df = df.reset_index(drop=True)
df.to_csv("pedidos_materia_prima_limpio.csv", index=False)

print("\n" + "=" * 60)
print("DESPUÉS DE LA LIMPIEZA")
print("=" * 60)
print(f"Filas totales: {len(df)}")
print(f"Filas duplicadas restantes: {df.duplicated().sum()}")
print(f"Filas eliminadas por cantidad_pedida nula/invalida: {filas_eliminadas_cantidad}")
print(f"Fechas de entrega imputadas con mediana por proveedor: {n_imputadas}")
print("\nValores nulos/vacíos por columna (después):")
for col in df.columns:
    print(f"  {col}: {df[col].isna().sum()}")
print("\nTipos de dato (después):")
print(df.dtypes)
print("\nValores únicos de 'proveedor' (después de normalizar):")
print(sorted(df['proveedor'].unique()))
print("\nValores únicos de 'estado' (después de normalizar):")
print(sorted(df['estado'].unique()))
