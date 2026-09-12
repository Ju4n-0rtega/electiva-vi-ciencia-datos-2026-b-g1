<!--
CONFIG
FULL_NAME: Juan Pablo Ortega Vargas
GITHUB_USER: Ju4n-0rtega
-->

# Actividad Práctica · Semana 2 — Clasifica datos y las V del Big Data

**Modalidad:** Individual
**Tipo:** Formativa (opcional, sin nota)
**Caso:** Logística y gestión de inventarios de materias primas en una empresa industrial

---

## 1. Fuentes de datos y clasificación

| # | Fuente de datos | Tipo |
|---|-------------------|------|
| 1 | Registros de inventario en el ERP (SKU, cantidad, ubicación, fecha) | Estructurado |
| 2 | Historial de ventas y órdenes de producción | Estructurado |
| 3 | Tiempos de entrega de proveedores (logs del sistema logístico) | Semiestructurado |
| 4 | Facturas y órdenes de compra de proveedores en PDF | Semiestructurado |
| 5 | Lecturas de sensores RFID/IoT en la bodega (entradas y salidas) | Semiestructurado |
| 6 | Correos electrónicos con proveedores sobre retrasos o cambios de pedido | No estructurado |
| 7 | Fotografías de productos dañados o mal recibidos | No estructurado |

Se listaron 7 fuentes, superando el mínimo de 6 solicitado, cubriendo los tres tipos de estructura de datos.

---

## 2. V del Big Data críticas en este caso

- **Volumen:** es crítico porque una empresa con varias bodegas y cientos de SKUs genera miles de registros de inventario y transacciones cada día; sin capacidad para manejar ese volumen, el análisis se vuelve inviable.
- **Velocidad:** es crítica porque los movimientos de entrada y salida de producto (especialmente los capturados por sensores RFID/IoT) ocurren de forma continua, y una decisión de reabastecimiento tardía puede provocar un desabastecimiento.
- **Veracidad:** es crítica porque una decisión de compra se basa directamente en los niveles de inventario reportados; si esos datos no son confiables, se pueden generar pedidos equivocados (de más o de menos).

Las otras dos V (variedad y valor) también aplican al caso, pero se consideran secundarias frente a estas tres para la decisión específica de reabastecimiento: la variedad es relevante porque existen datos estructurados, semiestructurados y no estructurados, pero no es lo que más urge resolver primero; el valor es el resultado esperado del análisis, no un reto a gestionar como tal.

---

## 3. Problema de veracidad y cómo detectarlo

**Problema de veracidad identificado:** el inventario físico real en la bodega puede no coincidir con el inventario registrado en el ERP, debido a errores de digitación, productos mal escaneados al recibirlos, o robos/pérdidas no reportados a tiempo.

**Cómo se detectaría:**
- Comparando periódicamente el inventario físico (conteo manual o mediante lectura de sensores RFID) contra el inventario registrado en el sistema, y midiendo la diferencia porcentual.
- Revisando si existen movimientos de entrada/salida sin un soporte asociado (por ejemplo, una salida de producto sin una orden de venta o de producción vinculada).
- Estableciendo un umbral de discrepancia aceptable (por ejemplo, más de un 5% de diferencia) que dispare una alerta automática para que el equipo de bodega revise y corrija el registro antes de que afecte una decisión de reabastecimiento.
