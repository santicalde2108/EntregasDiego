# Taller práctico: análisis de datos con Pandas

Programa de consola que lee datos de ventas y clientes, los limpia, los une y los analiza. Se ejecuta desde un menú en la terminal, y cada opción corresponde a un módulo que vas a completar paso a paso.

Recuerda consultar la guía adjunta en PDF donde se te dará el paso a paso del trabajo.

## Requisitos

- Python 3.10 o superior
- Git (para clonar el repositorio)
- Conocimientos básicos de variables, listas y funciones

## Cómo empezar

1. Clona el repositorio y entra a la carpeta del proyecto:

   ```
   git clone <URL-DEL-REPOSITORIO>
   cd <NOMBRE-DE-LA-CARPETA>
   ```

2. Crea y activa un ambiente virtual. Las instrucciones completas, para Windows y Mac/Linux, están en `LEEME_ambiente.txt`.

3. Instala las librerías:

   ```
   pip install -r requirements.txt
   ```

4. Ejecuta el programa:

   ```
   python main.py
   ```

Ejecuta siempre los comandos desde la carpeta del proyecto. Los módulos buscan los archivos a partir de su ubicación.

## Estructura del proyecto

```
├── main.py            Menú principal. No lo modifiques.
├── carga.py           Lee los CSV. Ya está completo.
├── limpieza.py        Limpia clientes y ventas. TODO 1 a 5.
├── merge.py           Valida y une las tablas. TODO 6 y 7.
├── analisis.py        Responde las preguntas de negocio. TODO 8 a 12.
├── graficos.py        Dibuja dos gráficos sencillos. TODO 13 y 14.
├── exploracion.py     Ejemplos de indexación, .loc, .iloc y concat. Se ejecuta por separado.
├── requirements.txt   Versiones de las librerías.
├── LEEME_ambiente.txt Pasos para crear el ambiente virtual.
└── Data/
    ├── raw/           Datos originales (cliente.csv, ventas.csv). No los modifiques.
    └── processed/     Resultados que genera el programa.
```

## Menú

| Opción | Qué hace |
|---|---|
| 1 | Carga los archivos CSV |
| 2 | Limpia los datos |
| 3 | Valida y une las tablas con merge |
| 4 | Muestra el análisis y las respuestas del desafío |
| 5 | Dibuja los gráficos de introducción |
| 6 | Sale del programa |

Las opciones se usan en orden: primero cargar (1), luego limpiar (2), después unir (3) y finalmente analizar (4) o graficar (5).

## Cómo completar el taller

1. Abre el archivo indicado en cada TODO. Cada función tiene un docstring con pistas.
2. Completa el TODO y ejecuta `python main.py` para probar la opción correspondiente.
3. Usa `exploracion.py` para practicar indexación, `.loc`, `.iloc` y `concat()` antes de aplicarlos en tu código.

Las funciones que aún no completaste no dan error: devuelven los datos sin cambios, así que el menú siempre funciona.

## Entregables

Consulta el documento del taller (`guia_Taller_Pandas.pdf`) para ver el detalle de cada entregable y la rúbrica. En resumen:

- Entregable 0: pantallazo del ambiente virtual activo y de la instalación.
- Entregable 1: pantallazos de `.shape`, `.info()` y `.describe()`, y salida de `exploracion.py`.
- Entregable 2: limpieza, con pantallazos antes y después y explicación.
- Entregable 3: validación, merge y análisis, con pantallazos de las opciones 3 y 4.
- Entregable 4: los dos gráficos (`.png`) y el código de `graficos.py`.
- Desafío final: respuestas a las cinco preguntas, con el criterio usado en cada una.

Para entregar, agrega al final de este `README.md` una sección con tu nombre y tus respuestas a las preguntas del desafío. Sube tus cambios al repositorio y envía el enlace por el formulario de entrega. La entrega es individual.

## Preguntas de negocio

1. ¿Qué categoría genera más ingresos?
2. ¿Qué canal vende más?
3. ¿Los clientes VIP compran más que los Regulares?
4. ¿Qué método de pago es el más usado?
5. ¿Cuáles son los cinco clientes con más compras?

---

## Desarrollo del taller y respuestas

**Estudiante:** Santiago Calderon

### Entregable 1: Exploración e indexación (`exploracion.py`)

- **Valores no nulos en `producto` (`ventas.csv`):** Al revisar `ventas.info()`, la tabla tiene 68 filas en total, pero la columna `producto` muestra **67 valores no nulos**, lo que indica que hay 1 registro con el nombre del producto vacío (la venta `V004`).
- **¿Por qué `.iloc[2, 6]` devuelve el total de la venta `V003`?:** Porque `.iloc` selecciona por posición numérica empezando a contar desde `0`. En las filas, la posición `0` es `V001`, la `1` es `V002` y la `2` corresponde a `V003`. En las columnas, después de hacer `ventas = ventas.set_index("id_venta")`, `id_venta` pasa a ser el índice y deja de contarse como columna; por lo tanto, el orden queda: `0` (`id_cliente`), `1` (`fecha_venta`), `2` (`producto`), `3` (`categoria`), `4` (`cantidad`), `5` (`precio_unitario`) y `6` (`total`). Así, `.iloc[2, 6]` devuelve `520000`.

### Entregable 2: Limpieza de datos (`limpieza.py`)

En la tabla de `clientes` (60 filas) no se encontraron valores nulos ni filas duplicadas; aun así se limpiaron posibles espacios en blanco en las columnas de texto con `.str.strip()`, se pasó la columna `ciudad` a formato título con `.str.title()` y se aseguraron filas únicas con `.drop_duplicates().reset_index(drop=True)`. En la tabla de `ventas` (68 filas) tampoco había duplicados, pero se encontró 1 valor nulo en la columna `producto` y la columna `fecha_venta` estaba como texto (`str`). El producto vacío se reemplazó por `"Sin especificar"` usando `.fillna()` en lugar de `.dropna()`, porque borrar la fila eliminaría una venta real por valor de $780.000 que sí tiene cliente, fecha, categoría y total válidos. Finalmente, `fecha_venta` se convirtió a tipo fecha (`datetime64`) con `pd.to_datetime()`.

### Entregable 3: Validación y Merge (`merge.py`)

- **Explicación del número de filas y columnas del merge:** El resultado del merge conserva las mismas **68 filas** de `ventas` porque se utilizó `how="left"` (manteniendo todas las ventas de la tabla izquierda) y en `clientes` cada `id_cliente` aparece una sola vez (`validate="m:1"`), evitando que se dupliquen ventas. En cuanto a las columnas, `ventas` tiene 10 columnas y `clientes` tiene 5 (que sumarían 15), pero la tabla unida queda con **14 columnas** porque `id_cliente` es la columna en común usada como llave (`on="id_cliente"`) y solo se incluye una vez.

---

### Respuestas al desafío final (Preguntas de negocio)

#### 1. ¿Qué categoría genera más ingresos?

```text
1. Ingresos por categoría:
categoria
Tecnologia    14290000
Hogar          3653000
Papeleria       749000
Accesorios      484000
Name: total, dtype: int64
Categoría con más ingresos: Tecnologia ($14290000)
```

- **Respuesta:** La categoría que genera más ingresos es **Tecnologia**, con un total de **$14.290.000**.
- **Criterio usado:** Se agruparon las ventas por la columna `categoria` con `groupby()`, se sumó el valor de la columna `total` (`.sum()`) y se ordenaron los resultados de mayor a menor.

#### 2. ¿Qué canal vende más?

```text
2. Ventas e ingresos por canal:
        ventas  ingresos
canal                   
Online      35  14669000
Tienda      33   4507000
```

- **Respuesta:** El canal que más vende es **Online**, superando a Tienda tanto en cantidad de transacciones (35 frente a 33) como en dinero recaudado ($14.669.000 frente a $4.507.000).
- **Criterio usado:** Se evaluaron ambos criterios (cantidad de ventas contando `id_venta` e ingresos sumando `total` por cada canal con `.agg()`). Online es el primero bajo cualquiera de los dos criterios, destacando especialmente por ingresos totales.

#### 3. ¿Los clientes VIP compran más que los Regulares?

```text
3. Comparación clientes VIP vs Regular:
                  clientes  compras  gasto_total  compras_por_cliente  gasto_por_cliente
segmento_cliente                                                                        
Regular                 36       39     11110000             1.083333      308611.111111
VIP                     24       29      8066000             1.208333      336083.333333
```

- **Respuesta:** Sí, en promedio los clientes **VIP** compran más que los Regulares: cada cliente VIP realiza en promedio **1,21 compras** y gasta **$336.083**, mientras que cada cliente Regular realiza **1,08 compras** y gasta **$308.611**.
- **Criterio usado:** Se comparó el promedio por cliente (dividiendo el total de compras y el gasto total de cada segmento entre la cantidad de clientes únicos obtenidos con `nunique()`), ya que comparar los totales brutos sería engañoso porque hay más clientes en el segmento Regular (36) que en el VIP (24).

#### 4. ¿Qué método de pago es el más usado?

```text
4. Ventas por método de pago:
metodo_pago
Efectivo         30
Tarjeta          25
Transferencia    13
Name: count, dtype: int64
Método de pago más usado: Efectivo (30 ventas)
```

- **Respuesta:** El método de pago más usado es **Efectivo**, con **30 ventas** (seguido por Tarjeta con 25 y Transferencia con 13).
- **Criterio usado:** Se contó el número de ventas registradas por cada categoría de la columna `metodo_pago` utilizando `.value_counts()`.

#### 5. ¿Cuáles son los cinco clientes con más compras?

```text
5. Top 5 clientes con más compras:
                             compras  gasto_total
id_cliente nombre_cliente                        
21         Nicolas Cardona         2      2515000
35         Matias Rodriguez        2      1278000
52         Mia Quintero            2      1090000
58         Luna Montoya            2      1007000
3          Luis Perez              2       730000
```

- **Respuesta:** Los cinco clientes con más compras son **Nicolas Cardona** ($2.515.000), **Matias Rodriguez** ($1.278.000), **Mia Quintero** ($1.090.000), **Luna Montoya** ($1.007.000) y **Luis Perez** ($730.000), todos con 2 compras realizadas.
- **Criterio usado:** Se agruparon las ventas por `id_cliente` y `nombre_cliente`, calculando la cantidad de compras (`count`) y el dinero total gastado (`sum`). Como había varios clientes empatados con 2 compras, se ordenó primero por número de compras de mayor a menor y se usó el `gasto_total` como criterio de desempate para seleccionar los 5 primeros con `.head(5)`.

---

### Bonus: Ventas por mes

```text
Bonus - Ventas por mes:
mes
2026-04    18234000
2026-05      942000
Freq: M, Name: total, dtype: int64
```

- **Respuesta:** El mes que más vendió fue **abril de 2026 (`2026-04`)** con **$18.234.000**, frente a mayo de 2026 (`2026-05`) que registró **$942.000** (usando `.dt.to_period("M")` sobre `fecha_venta` y sumando `total`).

