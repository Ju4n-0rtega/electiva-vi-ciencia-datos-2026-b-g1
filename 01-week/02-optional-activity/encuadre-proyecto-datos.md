<!--
CONFIG
FULL_NAME: Juan Pablo Ortega Vargas
GITHUB_USER: Ju4n-0rtega
-->

# Actividad Práctica · Semana 1 — Encuadra un proyecto de datos

**Modalidad:** Individual
**Tipo:** Formativa (opcional, sin nota)

---

## 1. Pregunta de negocio

¿Cuándo debería una empresa industrial generar un nuevo pedido de materia prima, y en qué cantidad, para evitar tanto el desabastecimiento que retrasa la producción como el exceso de inventario que incrementa los costos de almacenamiento?

Esta pregunta surge de un problema real de logística: las decisiones de reabastecimiento suelen tomarse de forma manual o por intuición, lo que genera errores costosos en ambos extremos (pedir de más o pedir tarde).

---

## 2. Datos necesarios y fuentes

| Dato necesario | Fuente |
|------------------|--------|
| Niveles actuales de inventario por producto | Sistema ERP / base de datos de bodega |
| Historial de ventas y consumo de materia prima | Sistema de ventas / órdenes de producción |
| Tiempos de entrega de cada proveedor | Registros logísticos / correos y órdenes de compra |
| Costos de almacenamiento y de pedido | Área financiera / contabilidad |
| Incidencias de entrega (retrasos, productos dañados) | Correos con proveedores y reportes de bodega |

---

## 3. Decisión esperada

Con base en el análisis de estos datos, se espera generar una recomendación automática de **"pedir ahora" o "esperar"**, junto con la **cantidad óptima a solicitar** para cada materia prima. Esta recomendación permitiría al área de compras tomar decisiones más rápidas y objetivas, reduciendo tanto el riesgo de parar la producción por falta de insumos como el costo de mantener inventario innecesario.

---

## 4. Tipo de analítica

Se requiere principalmente **analítica predictiva**, para estimar la demanda futura de cada materia prima a partir del historial de consumo y ventas. Complementariamente, se puede aplicar **analítica prescriptiva** para traducir esa predicción en una recomendación concreta de cuándo y cuánto pedir.
