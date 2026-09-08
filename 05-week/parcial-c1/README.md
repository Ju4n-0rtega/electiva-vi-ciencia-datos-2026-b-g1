<!--
CONFIG
FULL_NAME: Juan Pablo Ortega Vargas
GITHUB_USER: Ju4n-0rtega
-->

# Parcial Práctico · Corte 1 — Ciencia de Datos

**Modalidad:** Individual

**Caso elegido:** Logística y gestión de inventarios de materias primas en una empresa industrial

---

## 1. Tipos de datos identificados

| # | Dato / fuente | Tipo de dato | Justificación |
|---|----------------|--------------|----------------|
| 1 | Registros de inventario en el ERP (SKU, cantidad, ubicación, fecha) | Estructurado | Están organizados en tablas con campos fijos y un esquema definido |
| 2 | Lecturas de sensores IoT/RFID en la bodega (entradas y salidas de producto) | Semiestructurado | Llegan como eventos tipo log con metadatos, sin un esquema rígido de tabla |
| 3 | Correos electrónicos con proveedores sobre retrasos o cambios en un pedido | No estructurado | Es texto libre, sin campos ni estructura predefinida |
| 4 | Fotografías de productos dañados o mal recibidos | No estructurado | Son imágenes, no tienen forma tabular ni campos |

---

## 2. Preguntas de analítica

**Analítica descriptiva:**
¿Cuál fue el nivel promedio de inventario por semana durante el último trimestre?

**Analítica predictiva:**
¿Cuál será la demanda estimada de una materia prima específica durante las próximas 4 semanas, con base en el historial de ventas y producción?

---

## 3. Diagrama del flujo de datos

Fuente → Almacenamiento → Análisis → Visualización

```mermaid
flowchart LR
    A["Fuente
    ERP, sensores IoT, correos con proveedores"] --> B["Almacenamiento
    Base de datos / Data lake"]
    B --> C["Análisis
    Modelos descriptivos y predictivos"]
    C --> D["Visualización
    Dashboard de niveles de inventario y alertas"]
```

- **Fuente:** el ERP registra inventario y órdenes, los sensores IoT capturan movimientos en tiempo real, y los correos aportan contexto sobre retrasos de proveedores.
- **Almacenamiento:** toda la información se centraliza en una base de datos o data lake para poder cruzarla.
- **Análisis:** se aplican modelos descriptivos (qué ha pasado) y predictivos (qué va a pasar) sobre esos datos.
- **Visualización:** los resultados se muestran en un dashboard con niveles de inventario, tendencias y alertas de stock crítico.

---

## English section

- Descriptive analytics looks at historical inventory and sales data to summarize what has already happened, such as average stock levels over the last quarter.
- Predictive analytics uses that same historical data to build models that estimate future outcomes, such as forecasting how much raw material will be needed in the coming weeks.
