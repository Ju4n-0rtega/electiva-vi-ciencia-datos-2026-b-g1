<!--
CONFIG
FULL_NAME: Juan Pablo Ortega Vargas
GITHUB_USER: Ju4n-0rtega
-->

# Actividad Calificable · Corte 1 — Diagnóstico de datos de un proceso

**Curso:** Electiva VI [Ciencia de Datos] · Corte 1
**Proceso elegido:** Logística y gestión de inventarios

---

## 1. Proceso y pregunta de datos

**Proceso:** Logística industrial — gestión de inventarios de materias primas.

**Pregunta de datos:**
¿Cuándo debería generarse un nuevo pedido de materia prima y qué cantidad debería solicitarse, de manera que se minimicen los costos de almacenamiento y se evite el desabastecimiento que genera retrasos en producción?

Esta pregunta es relevante porque una mala decisión de reabastecimiento genera dos tipos de pérdidas opuestas: sobre-stock (capital inmovilizado, costos de almacenamiento, riesgo de obsolescencia) o desabastecimiento (paros de producción, incumplimiento de entregas, clientes insatisfechos). Contar con datos y analítica adecuada permite encontrar el punto óptimo entre ambos extremos.

---

## 2. Inventario de datos

| # | Fuente / campo de datos | Tipo de dato | Justificación |
|---|--------------------------|--------------|----------------|
| 1 | Niveles actuales de inventario (bodega) | Estructurado | Registros tabulares en base de datos (SKU, cantidad, ubicación, fecha) |
| 2 | Historial de ventas / salidas de producto | Estructurado | Tablas transaccionales con campos fijos (fecha, producto, cantidad, cliente) |
| 3 | Órdenes de producción | Estructurado | Registros en sistema ERP con campos definidos (orden, cantidad requerida, fecha) |
| 4 | Tiempos de entrega de proveedores (logs del sistema logístico / API de transportadora) | Semiestructurado | Datos en formato JSON/XML con jerarquía variable entre proveedores |
| 5 | Facturas y órdenes de compra de proveedores en PDF | Semiestructurado | Tienen campos identificables (fecha, ítems, valores) pero no están en una tabla rígida |
| 6 | Correos electrónicos con proveedores sobre retrasos o cambios de pedido | No estructurado | Texto libre, sin un esquema fijo de campos |
| 7 | Fotografías de productos dañados o mal recibidos | No estructurado | Imágenes, sin estructura tabular |
| 8 | Lecturas de sensores RFID/IoT en bodega (entradas y salidas en tiempo real) | Semiestructurado | Flujo continuo de eventos con metadatos, formato tipo log |

Con 8 fuentes identificadas se cumple ampliamente el mínimo de 6 solicitado, cubriendo los tres tipos de dato (estructurado, semiestructurado y no estructurado).

---

## 3. Tipo de analítica y justificación de Big Data

### Tipo de analítica aplicada

- **Analítica predictiva:** a partir del historial de ventas, órdenes de producción y tiempos de entrega, se puede construir un modelo que **estime la demanda futura** de cada materia prima (por ejemplo, para las próximas 4 semanas).
- **Analítica prescriptiva:** una vez estimada la demanda, el sistema puede **recomendar automáticamente** el punto de reorden (cuándo pedir) y la cantidad óptima a solicitar (cuánto pedir), considerando tiempos de entrega y costos de almacenamiento.

Se usan ambos tipos de manera complementaria: la predictiva responde "¿qué va a pasar?" y la prescriptiva responde "¿qué debo hacer al respecto?".

### ¿Es un caso de Big Data?

Sí, puede considerarse un caso de Big Data cuando la empresa maneja múltiples bodegas, cientos o miles de SKUs y transacciones continuas. Se justifica con las 5 V:

- **Volumen:** miles de registros diarios de inventario, ventas y movimientos entre varias bodegas.
- **Velocidad:** las entradas y salidas de producto, así como los pedidos, cambian de forma constante y en algunos casos en tiempo real (sensores RFID).
- **Variedad:** coexisten datos numéricos (inventario, ventas), semiestructurados (logs, facturas) y no estructurados (correos, fotos de productos averiados).
- **Veracidad:** los datos deben ser confiables, ya que un registro de inventario erróneo puede llevar a pedir de más, de menos, o en el momento equivocado.
- **Valor:** el análisis permite reducir costos de almacenamiento, evitar desabastecimientos y mejorar la planeación de la producción, generando un beneficio económico directo.

---

## 4. Ciclo de vida del proyecto de datos

1. **Pregunta:** ¿Cuándo y cuánto pedir de cada materia prima para minimizar costos y evitar desabastecimiento?
2. **Obtener:** recolectar datos de inventario, ventas, órdenes de producción, tiempos de entrega de proveedores, correos y fotografías de incidencias, y lecturas de sensores de bodega.
3. **Limpiar:** unificar formatos de fecha, eliminar duplicados en transacciones, estandarizar nombres de proveedores y productos, extraer campos clave de facturas en PDF y filtrar correos irrelevantes.
4. **Analizar:** aplicar modelos de pronóstico de demanda (analítica predictiva) y reglas/modelos de optimización de punto de reorden y cantidad económica de pedido (analítica prescriptiva).
5. **Visualizar:** construir dashboards con niveles de inventario en el tiempo, alertas de stock crítico y comparación entre demanda proyectada vs. real.
6. **Decidir:** generar automáticamente la recomendación de "pedir ahora / esperar" y la cantidad sugerida, apoyando la decisión del área de compras y logística.

---

## Problem & data (English section)

Our team is analyzing the raw-material inventory management process in an industrial company, focusing on when to place a new purchase order and how much to order. Poor decisions in this process lead either to excess inventory and higher storage costs, or to stockouts that delay production. To support this decision, we need data from several sources: current inventory levels, sales history, production orders, supplier delivery times, purchase invoices, supplier emails, photos of damaged goods, and warehouse sensor logs. These sources include structured data such as inventory and sales tables, semi-structured data such as delivery logs and invoices, and unstructured data such as emails and images. We plan to use predictive analytics to forecast future demand for each raw material, and prescriptive analytics to automatically recommend the reorder point and the optimal order quantity. Combining these analytics types should help the company reduce storage costs, avoid production stoppages, and make faster, data-driven purchasing decisions.
