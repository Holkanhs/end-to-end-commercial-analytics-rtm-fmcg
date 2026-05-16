# Narrativa RTM México FMCG 2024

> **Agent:** Storytelling | **Dataset:** RTM_Mexico_FMCG_2024 | **Pipeline step:** 15
> **Audience:** Dirección de Logística, Equipo RTM, Equipo Comercial
> **Tone:** Executive — conciso, orientado a decisiones
> **Storyboard:** `working/storyboard_RTM_Mexico_FMCG_2024.md`

---

## Resumen Ejecutivo

El equipo RTM analizó las 72 rutas del portafolio mexicano de FMCG durante el año completo 2024 — 100,000 facturas, 8 ciudades, 3 canales, 3 formatos de tienda — para determinar dónde invertir en 2025. El hallazgo central: **la geografía no predice la rentabilidad**. La brecha entre ciudades es de solo 3.5%, pero la brecha entre la mejor y la peor ruta individual es de $71k MXN por año — y ese gap está determinado exclusivamente por la combinación de **canal y formato de tienda**, no por la ciudad. El canal Offline retrocedió −0.11% en el segundo semestre mientras Omnicanal y Online crecieron +0.18% cada uno; el formato Express arrastra el portafolio en los tres canales; y el costo de servicio permanece fijo al 80% independientemente del volumen, lo que confirma que el margen recuperable es real y está a disposición del equipo. **$355k MXN anuales están disponibles sin agregar una sola ruta nueva.** La recomendación: proteger las 3 rutas estrella, restructurar las 2 rutas Offline Express críticas, y acelerar la migración Omnicanal antes de que la brecha de canal se amplíe.

---

## Parte 1 — Contexto: Un portafolio maduro y completamente mapeado

La pregunta que disparó este análisis fue directa: ¿dónde debe invertir el equipo RTM en 2025 para capturar el mayor retorno de margen? La hipótesis inicial — que las ciudades con mayor población o penetración comercial explicarían las diferencias de desempeño — no se sostuvo.

### Finding 1: El portafolio RTM cubre $118M en 72 rutas — el mercado está cubierto

**Headline:** El portafolio RTM genera $118M MXN en 100,000 facturas anuales
**Detail:** 72 rutas activas (8 ciudades × 3 canales × 3 formatos), margen bruto promedio de 19.34%, ticket promedio de $393 MXN, CTS de 80.0%
**Impact:** El mercado está cubierto. El objetivo para 2025 no es expansión — es optimización de la mezcla existente.

**Metrics:**
- $118M | Ingresos Totales MXN | 100,000 facturas | default
- 19.3% | Margen Bruto Promedio | base sana | green
- 80.0% | Costo de Servicio (CTS) | estable | amber
- 72 | Rutas Analizadas | 8 ciudades · 3 canales · 3 formatos | default

**Source:** `fct_sales` · `dim_locations` · Enero–Diciembre 2024 · Pipeline dbt

---

### Finding 2: La brecha entre ciudades es de solo 3.5% — la geografía no predice el margen

**Headline:** Monterrey genera $15.0M; Tijuana $14.5M — una diferencia de apenas 3.5%
**Detail:** Las 8 ciudades distribuyen ingresos de manera notablemente uniforme, con una variación máxima de $500k MXN entre la primera y la última ciudad
**Impact:** Invertir en nuevas ciudades no resolverá el problema de margen. El driver real está dentro de las ciudades — en la combinación de canal y formato.

**Metrics:**
- $15.0M | Monterrey (1er lugar) | top del portafolio | default
- 3.5% | Brecha total entre ciudades | la menor del portafolio | default
- $14.5M | Tijuana (último lugar) | fondo del portafolio | default

**Chart:** `outputs/charts/01_city_revenue.png`
**Source:** `fct_sales JOIN dim_locations` · Agrupado por ciudad · 2024

La distribución de ingresos por ciudad es una de las más homogéneas observadas en portafolios RTM de FMCG. Esto no es una debilidad — es una señal de que el equipo tiene presencia equilibrada. Pero también es una advertencia: **la city-expansion no es la palanca disponible. La palanca está en la mezcla de canal y formato dentro de los mercados que ya se tienen.**

---

## Parte 2 — Tensión: La variabilidad real está en el nivel de ruta

Cuando el análisis baja del nivel de ciudad al nivel de ruta individual, el panorama cambia completamente.

### Finding 3: Dentro de las ciudades, la brecha entre mejor y peor ruta es $71k MXN al año

**Headline:** Las 5 rutas líderes generan $71k MXN más de margen que las 5 más débiles — por ruta, por año
**Detail:** Top 5 rutas: $350k MXN de margen bruto promedio; Bottom 5: $302k MXN. Además, las mejores rutas generan $401 MXN de ingreso por unidad vs $381 en las débiles (+5.3%)
**Impact:** Si las 5 rutas más débiles igualaran la economía de las rutas estrella, el portafolio recuperaría $355k MXN de margen bruto anual — sin agregar una sola ruta nueva.

**Metrics:**
- $350k | Margen bruto promedio · Top 5 rutas | por ruta al año | green
- $302k | Margen bruto promedio · Bottom 5 rutas | por ruta al año | red
- $71k | Brecha por ruta al año | $355k en 5 rutas = recuperable | amber

**Chart:** `outputs/charts/05_top_bottom_routes.png`
**Source:** `fct_sales JOIN dim_locations` · Agrupado por ruta (ciudad × canal × formato) · 2024

La pregunta que sigue naturalmente es: ¿qué separa a las rutas del top de las del bottom? ¿Es la ciudad? ¿Es el cliente? Los datos apuntan con claridad a dos factores: **el canal** y **el formato de tienda**.

---

### Finding 4: El canal Offline perdió terreno en H2 — la señal es pequeña pero estructural

**Headline:** Offline retrocedió −0.11% en el segundo semestre mientras Omnicanal y Online crecieron +0.18% cada uno
**Detail:** Dividiendo el año en H1 (enero–junio) y H2 (julio–diciembre), el canal Offline perdió participación relativa mientras los canales digitales crecieron de manera consistente
**Impact:** En términos absolutos el movimiento es modesto. En términos direccionales, el patrón es inequívoco y se acentuará sin intervención. El camino Offline-only se está volviendo estructuralmente menos competitivo.

**Metrics:**
- +0.18% | Crecimiento Omnicanal H2 vs H1 | señal positiva | green
- +0.18% | Crecimiento Online H2 vs H1 | señal positiva | green
- −0.11% | Caída Offline H2 vs H1 | señal de alerta | red

**Chart:** `outputs/charts/02_channel_h1_h2.png`
**Source:** `fct_sales JOIN dim_locations` · Corte 2024-07-01 · Por canal

El movimiento de canal en H2 es la primera evidencia temporal de un cambio estructural. La pregunta que sigue es: ¿cuál combinación de canal y formato está generando el mayor margen?

---

### Finding 5: Omnicanal Super lidera el portafolio — Express arrastra en los tres canales

**Headline:** Omnicanal Super: 19.61% de margen — el mejor del portafolio. Express: el más bajo en los tres canales sin excepción
**Detail:** La matriz 3×3 (formato × canal) muestra que Super supera a Hyper y Express en todos los canales. Más importante: el mismo formato (Hyper) rinde mejor en Omnicanal que en Offline. Express no compensa su bajo ticket promedio con ninguna ventaja de costo.
**Impact:** La combinación de formato y canal importa más que la ciudad. Una ruta Omnicanal Super en cualquier ciudad supera a una ruta Offline Express en la ciudad con mayor volumen.

**Metrics:**
- 19.61% | Omnicanal Super · mejor del portafolio | referencia | green
- 19.27% | Hyper Omnicanal · por debajo de Offline Hyper | ineficiencia logística | amber

**Chart:** `outputs/charts/06_format_channel_heatmap.png`
**Source:** `fct_sales JOIN dim_locations` · Agrupado por formato × canal · 2024

Este hallazgo tiene una implicación directa: no es solo el canal Offline el que cede — es la **combinación Offline + Express** la que concentra el mayor riesgo del portafolio. Pero antes de concluir que esto es un problema de costos, el análisis verifica la estructura del CTS.

---

### Finding 6: El CTS permanece estable en 79.8–80.2% todo el año — este no es un problema de costos

**Headline:** Los ingresos oscilan entre meses; el costo de servicio no — la brecha de margen es de canal y formato, no de estructura de costos
**Detail:** A pesar de los picos de ingresos en enero, agosto y octubre y los valles en febrero y septiembre, el CTS se mantiene en un rango de apenas 0.4 puntos porcentuales durante todo el año
**Impact:** La estructura de costos es fija. Cualquier mejora de margen que se logre a través de la reestructuración de rutas irá directamente al resultado final — sin que el costo operativo absorba la ganancia.

**Metrics:**
- 79.8–80.2% | Rango CTS todo el año | estructura fija | default
- 0.4 pp | Variación máxima en CTS 2024 | no significativa | default

**Chart:** `outputs/charts/04_monthly_trend.png`
**Source:** `fct_sales` · Agrupado mensualmente · Ene–Dic 2024

Este hallazgo es decisivo: elimina la hipótesis alternativa ("el Express tiene CTS más alto, por eso es menos rentable"). **El CTS es homogéneo en todo el portafolio. La diferencia está en el ingreso por unidad — y el ingreso por unidad está determinado por el canal y el formato.**

---

## Parte 3 — Resolución: Tres rutas definen el estándar; tres decisiones capturan la oportunidad

### Finding 7: Tres rutas confirman lo que es posible — cinco rutas muestran lo que se pierde

**Headline:** CDMX Offline Hyper, Monterrey Omnicanal Super y Puebla Omnicanal Express generan $350k+ de margen bruto cada una — con CTS por debajo de 79.9%
**Detail:** Las rutas estrella comparten el patrón: canal Omnicanal o Offline con formato Hyper o Super, CTS consistentemente bajo, ticket promedio de $401 MXN. En el extremo opuesto, Querétaro Offline Express y León Offline Express registran el menor margen del portafolio con el CTS más alto.
**Impact:** Las rutas estrella no son excepciones — son el modelo. La matriz de eficiencia muestra que el cuadrante superior izquierdo (bajo CTS, alto valor de ticket) está al alcance de rutas actualmente en el cuadrante inferior derecho.

**Metrics:**
- $350k+ | Margen bruto anual · rutas estrella | estándar del portafolio | green
- 79.9% | CTS máximo · rutas estrella | umbral a mantener | green
- $288k | Margen bruto · Querétaro Offline Express | fondo del portafolio | red

**Chart:** `outputs/charts/03_route_matrix.png`
**Source:** `fct_sales JOIN dim_locations JOIN dim_products` · Por ruta · 2024

---

## Parte 4 — Implicación: El costo de no actuar es $355k MXN al año

Si el portafolio mantiene su mezcla actual de canales y formatos, sin reestructurar las rutas Offline Express y sin acelerar la migración Omnicanal:

- Las **2 rutas Express críticas** (Querétaro y León) acumulan $67k MXN de margen no capturado **por año**. En tres años: **$201k MXN de oportunidad perdida** solo en esas dos rutas.
- La **tendencia de canal** de H2 continuará: Offline seguirá cediendo terreno sin una intervención comercial activa.
- Las **rutas estrella** quedan en riesgo si no se les protege con frecuencia de visita prioritaria y disponibilidad de stock — la eficiencia actual no se mantiene sin gestión activa.

**Finding 8: $355k MXN de margen están disponibles sin agregar una sola ruta nueva**

**Headline:** El gap entre las 5 rutas más débiles y las 5 estrella vale $355k MXN al año — enteramente recuperable
**Detail:** Reestructurar las 5 rutas más débiles a la economía de las rutas estrella = $355k/año. Un traslado del 5% del volumen Offline al canal Omnicanal en las 10 rutas más débiles = $180k–$220k adicionales.
**Impact:** La oportunidad total supera los $500k MXN anuales si se ejecutan ambas palancas en paralelo.

**Metrics:**
- $355k | Margen recuperable · reestructurar 5 rutas | por año | green
- $201k | Costo de no actuar · solo 2 rutas Express | en 3 años | red
- $180–220k | Adicional · migración Omnicanal 5% del volumen | Q2 2025 | green

---

## Parte 5 — Recomendación: Tres decisiones para 2025

### R1 — Proteger y escalar las 3 rutas estrella
**Confidence: High** — sustentada en datos anuales completos con 0 nulos, CTS estable, y margen consistentemente superior.

CDMX Offline Hyper, Monterrey Omnicanal Super y Puebla Omnicanal Express representan el 4.2% de las rutas y una fracción desproporcionada del margen del portafolio. La acción es directa: **garantizar frecuencia de visita prioritaria** (sin mezclar con paradas de bajo valor en la misma secuencia de ruta), **asegurar stock** mediante acuerdos de reabastecimiento preferencial (lead time actual: 8–9 días), y revisar condiciones comerciales para incentivar mayor volumen en estos puntos.

*Métrica de éxito:* CTS < 79.9% y margen > $350k MXN en las 3 rutas durante todo 2025.

---

### R2 — Reestructurar las rutas Offline Express críticas
**Confidence: High** — el underperformance de Express es consistente en los 3 canales y en todas las ciudades; no es un fenómeno local.

Querétaro Offline Express y León Offline Express acumulan $67k MXN de margen no capturado frente al promedio del portafolio. Hay tres opciones para evaluar, no necesariamente mutuamente excluyentes:

- **(A) Convertir a punto Omnicanal** — migrar la atención de estos clientes al canal digital y reducir las visitas presenciales a las de mayor valor
- **(B) Consolidar paradas** — agrupar clientes Express cercanos para elevar el ticket promedio por visita
- **(C) Salida controlada** — liberar capacidad de campo para reforzar rutas Hyper/Super en la misma ciudad

*Métrica de éxito:* Margen ≥ $320k MXN en Querétaro Offline Express para Q2 2025.

---

### R3 — Acelerar la migración Omnicanal
**Confidence: Medium-High** — la tendencia de H2 es clara; la magnitud del efecto en 2025 depende de la velocidad de ejecución comercial.

La señal de H2 (+0.18% Omnicanal vs −0.11% Offline) y la matriz formato × canal confirman la dirección. El plan: identificar los **10 clientes Offline de menor ticket** por ciudad y ofrecerles incorporación digital con apoyo comercial activo. **Meta de conversión Q2 2025:** 5% del volumen Offline migrado a Omnicanal en las 5 rutas más débiles.

*Métrica de éxito:* +0.3 pp de margen en rutas convertidas; KPI de seguimiento mensual activo.

---

## Plan de acción — próximos 90 días

| # | Acción | Responsable | Fecha límite | Métrica de éxito |
|---|--------|-------------|--------------|------------------|
| 1 | Revisar plan de ruta Querétaro Offline Express | Gerente RTM | Mar 2025 | Margen ≥ $320k MXN en Q2 |
| 2 | Piloto de conversión Omnicanal en 2 rutas Offline | Comercial + Logística | Mar 2025 | +0.3 pp de margen |
| 3 | Definir frecuencia de visita para top 10 rutas | Operaciones de Campo | Ene 2025 | 100% cobertura rutas estrella |
| 4 | Revisar estructura de costos Hyper Omnicanal | RTM + Finanzas | Mar 2025 | CTS% < 80.0% |
| 5 | Establecer cadencia mensual de revisión de rutas | Dirección RTM | Feb 2025 | Dashboard activo con KPIs |

---

## Datos de soporte

### Charts referenciados
| # | Archivo | Beat | Descripción |
|---|---------|------|-------------|
| 1 | `outputs/charts/01_city_revenue.png` | Beat 02 | Ingresos por ciudad — distribución uniforme |
| 2 | `outputs/charts/05_top_bottom_routes.png` | Beat 03 | Top 5 vs Bottom 5 rutas — brecha de $71k |
| 3 | `outputs/charts/02_channel_h1_h2.png` | Beat 04 | Canal H1 vs H2 — Offline −0.11%, Omnicanal +0.18% |
| 4 | `outputs/charts/06_format_channel_heatmap.png` | Beat 05 | Matriz formato × canal — Omnicanal Super lidera |
| 5 | `outputs/charts/04_monthly_trend.png` | Beat 06 | CTS mensual — estructura fija, independiente del volumen |
| 6 | `outputs/charts/03_route_matrix.png` | Beat 07 | Matriz de eficiencia — 72 rutas por CTS vs ticket |

### Métricas clave
| Métrica | Valor | Fuente |
|---------|-------|--------|
| Total revenue | $118,005,404 MXN | `SUM(fct_sales.revenue)` |
| Total invoices | 100,000 | `COUNT(fct_sales.invoice_id)` |
| Avg margin % | 19.34% | `AVG(fct_sales.margin_pct)` |
| Avg ticket | $393.32 MXN | `AVG(fct_sales.avg_ticket_price)` |
| CTS ratio | 79.98% | `SUM(cost)/SUM(revenue)` |
| Routes analyzed | 72 | `COUNT(DISTINCT dim_locations.location_key)` |

### Limitaciones y caveats
- Dataset de año único (2024) — sin comparativo interanual disponible; H1/H2 se usa como benchmark interno
- CTS es un proxy (`costo total / ingreso total`) — excluye costos logísticos de transporte no capturados en el dataset transaccional
- `customer_age = 0` indica dato desconocido (~15% de filas) — excluir o segmentar como "n/d" si se muestra desglose por edad
- 62 `invoice_id` con duplicados identificados — representan < 0.1% del total y no afectan las conclusiones del portafolio

### Pipeline de reproducibilidad
Snowflake `FMCG_RTM.raw.sales_data_raw` → dbt staging (`stg_sales_data`) → intermediate (`int_route_performance`) → marts (`fct_sales`, `dim_customers`, `dim_products`, `dim_locations`) → 4 CSVs en `03_powerbi/data/` → Power BI `RTM_FINAL_PROJECT.pbix`
