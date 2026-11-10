# Taller práctico proyecto integrador: calidad de datos para la retención estudiantil

Una institución de educación superior quiere entender qué factores están asociados a la deserción, para diseñar estrategias de retención tempranas. Antes de responder preguntas de análisis, el equipo de datos debe garantizar que la información sea confiable. Este taller trabaja justo ese paso: auditar, limpiar y documentar los datos, y después responder cinco preguntas con esos datos limpios.

Los datos son sintéticos. Fueron generados para el taller y no corresponden a estudiantes reales.

## Requisitos

- Python 3.10 o superior
- Git
- Lo visto en los talleres de Pandas y de limpieza de datos

## Cómo empezar

1. Clona el repositorio y entra a la carpeta del proyecto:

   ```
   git clone <URL-DEL-REPOSITORIO>
   cd <NOMBRE-DE-LA-CARPETA>
   ```

2. Crea y activa un ambiente virtual. Las instrucciones para Windows y Mac/Linux están en `LEEME_ambiente.txt`.

3. Instala las librerías:

   ```
   pip install -r requirements.txt
   ```

4. Ejecuta el script:

   ```
   python analisis_desercion.py
   ```

Ejecuta el comando desde la carpeta del proyecto.

## Estructura del proyecto

```
proyecto/
├── analisis_desercion.py   Script principal. Tiene un TODO por cada paso.
├── requirements.txt        Versiones de las librerías.
├── LEEME_ambiente.txt      Pasos para crear el ambiente virtual.
├── README.md               Este archivo.
├── .gitignore              Archivos que Git no debe subir.
└── Data/
    ├── raw/
    │   └── datos_estudiantes.csv   Dataset original. No lo modifiques.
    └── processed/
        ├── .gitkeep                Mantiene la carpeta en el repositorio.
        ├── dataset_limpio.csv      Lo genera el script. No se sube (está en .gitignore).
        ├── decisiones.csv          Lo genera el script. Sí se sube.
        └── graficos/               Lo genera el script. Sí se sube.
```

Lo que genera el script (`dataset_limpio.csv`, `decisiones.csv` y `graficos/`) aparece en `Data/processed/` al ejecutarlo. Los dos últimos se suben al repositorio, porque son parte de la entrega.

## Qué debes hacer

Completa los TODO de `analisis_desercion.py` en orden. Cada función tiene un docstring con preguntas: respóndelas antes de escribir el código. Cada decisión que tomes debe quedar registrada con `registrar()`.

Cuando termines, el script debe producir:

- `Data/processed/dataset_limpio.csv`: el dataset limpio.
- `Data/processed/decisiones.csv`: la tabla de decisiones.
- `Data/processed/graficos/`: los cuatro gráficos.

La guía del taller (`Taller_Retencion_Estudiantil.docx`) explica cada método antes de usarlo, con ejemplos y errores frecuentes.

## Entrega

Sube tu código completo al repositorio y envía el enlace por el formulario de entrega. La entrega es individual.

El repositorio debe incluir:

- `analisis_desercion.py` con todos los TODO completados.
- `Data/processed/decisiones.csv` y la carpeta `Data/processed/graficos/`.
- Un `README.md` al final de este archivo, con una sección titulada **Mis decisiones y respuestas**. Debe incluir:
  0. El diccionario de datos: la tabla de las 23 columnas con tipo, descripción y rol, completada según el paso 1 de la guía.
  1. Tu diagnóstico de calidad: qué problemas encontraste y en qué columnas.
  2. Tus decisiones de limpieza, con su justificación.
  3. Las respuestas a las cinco preguntas, cada una con el número de estudiantes por grupo.
  4. Tu respuesta a la reflexión sobre asociación y causalidad.
  5. Tu respuesta a la reflexión sobre `motivo_retiro` y la predicción.
  6. Tu respuesta a la reflexión sobre el uso de variables sensibles.

El script debe ejecutarse sin errores desde cero. Cada decisión necesita una justificación, y cada conclusión debe apoyarse en un número del análisis.

---

## Mis decisiones y respuestas

### 0. Diccionario de datos

| Columna | Tipo | Descripción | Rol |
| :--- | :--- | :--- | :--- |
| `id_estudiante` | texto | Código único que identifica a cada estudiante en la institución | identificación |
| `programa` | categórica | Carrera o programa académico en el que está matriculado el estudiante | explicativa |
| `facultad` | categórica | Facultad a la que pertenece el programa académico | explicativa |
| `jornada` | categórica | Horario en el que estudia (Diurna, Nocturna o Fin de semana) | explicativa |
| `semestre` | numérica | Semestre actual que cursa el estudiante (de 1 a 10) | explicativa |
| `promedio_acumulado` | numérica | Nota promedio acumulada en la carrera en escala de 0 a 5 | explicativa |
| `creditos_aprobados` | numérica | Cantidad total de créditos que el estudiante ya aprobó | explicativa |
| `materias_reprobadas` | numérica | Cantidad de materias perdidas durante la carrera | explicativa |
| `asistencia_pct` | numérica | Porcentaje de asistencia a clase (llega como texto por símbolos `%` y `-`) | explicativa |
| `sesiones_tutoria` | numérica | Número de tutorías académicas a las que ha asistido | explicativa |
| `cambios_programa` | numérica | Veces que el estudiante se ha cambiado de carrera | explicativa |
| `estrato` | categórica | Estrato socioeconómico del estudiante (de 1 a 6, aunque venga con números) | explicativa |
| `beca` | categórica | Indica si el estudiante tiene beca o apoyo económico (`sí` o `no`) | explicativa |
| `trabaja` | categórica | Indica si el estudiante trabaja actualmente (`sí` o `no`) | explicativa |
| `horas_trabajo_semana` | numérica | Horas que trabaja a la semana (llega como texto porque usa `-` cuando no aplica) | explicativa |
| `distancia_km` | numérica | Distancia en kilómetros desde donde vive hasta la institución | explicativa |
| `edad` | numérica | Edad del estudiante en años | explicativa |
| `genero` | categórica | Género registrado del estudiante (`Femenino` o `Masculino`) | explicativa |
| `ciudad_procedencia` | categórica | Municipio o ciudad de origen del estudiante | explicativa |
| `tipo_colegio` | categórica | Tipo de colegio del que se graduó (`Público` o `Privado`) | explicativa |
| `fecha_matricula` | fecha | Fecha en la que realizó la matrícula | explicativa |
| `estado` | categórica | Situación actual del estudiante: `activo`, `desertor` o `graduado` | resultado |
| `motivo_retiro` | categórica | Razón por la que se retiró (solo aplica cuando el estado es `desertor`) | resultado |

### 1. Diagnóstico de calidad

Al revisar el archivo original (`10150` filas y `23` columnas), aparecieron los seis tipos de problemas vistos en la guía:

- **Duplicados:** El dataset trae `150` filas completamente repetidas (incluso con el mismo `id_estudiante`), por eso hay 10150 registros en vez de 10000 estudiantes únicos.
- **Nulos reales (`isnull().sum()`):**
  - `promedio_acumulado`: `304` nulos (`298` después de quitar duplicados). Son errores porque todo estudiante debería tener registro de su promedio.
  - `distancia_km`: `199` nulos reales.
  - `ciudad_procedencia`: `103` nulos reales (`100` sin duplicados).
  - `tipo_colegio`: `152` nulos reales (`150` sin duplicados).
  - `motivo_retiro`: `6877` nulos (`6764` sin duplicados). Estos nulos **no son un error**, sino nulos esperados, porque la pregunta solo aplica para los `3273` estudiantes que desertaron; en el mapa de faltantes (`mapa_faltantes.png`) se ve claramente que es la columna con más espacios vacíos junto con los pequeños huecos de promedio, distancia, ciudad y colegio.
- **Faltantes disfrazados:**
  - En `asistencia_pct` hay `202` celdas con un guion (`-`) en lugar de estar vacías.
  - En `horas_trabajo_semana` hay `2822` celdas con guion (`-`), todas en filas donde `trabaja` es `no`.
  - En `distancia_km` aparece `152` veces el número `999`, que se usó como código para indicar que no había dato.
- **Formato inconsistente:**
  - `asistencia_pct` y `horas_trabajo_semana` llegan como texto (`str`). En `asistencia_pct`, además de los guiones, hay `300` registros con el signo `%` pegado al número.
  - `fecha_matricula` mezcla dos formatos distintos: `7098` fechas están en `AAAA-MM-DD` y `3052` en `DD/MM/AAAA`.
- **Errores tipográficos en categorías:**
  - `programa`: `260` filas escritas sin tilde (`Ingenieria de Sistemas` en 144 filas y `Psicologia` en 116).
  - `jornada`: `485` filas con variaciones de mayúsculas, minúsculas o espacios (`diurna` en 318, `nocturna` en 89 y `NOCTURNA ` con espacio al final en 78).
  - `genero`: `559` filas fuera del formato estándar (`M` en 239, `F` en 167 y `femenino` en minúscula en 153).
  - `ciudad_procedencia`: `542` filas con variantes como `BOGOTÁ` (128), `Bogota` (120), `bogota ` con espacio (118), `medellin` (90) y `Medellin ` con espacio (86).
- **Valores imposibles:**
  - `promedio_acumulado`: `17` filas (`15` después de quitar duplicados y nulos) tienen valores mayores a 5 (`45.0` en 1 fila, `62.0` en 8 filas y `78.0` en 6 filas), cuando la escala de notas va de 0 a 5.
  - `edad`: `12` filas están fuera de un rango razonable de 15 a 60 años (`4` registros con `12` años y `8` registros con `150` años).
  - `horas_trabajo_semana`: `30` filas (`29` después de limpiar promedio) tienen `200` horas semanales, lo cual es imposible porque una semana completa solo tiene 168 horas.

### 2. Decisiones de limpieza y justificación

1. **Conversión a numérico (`asistencia_pct`, `horas_trabajo_semana`, `distancia_km`):**
   - En `asistencia_pct` se quitó el símbolo `%` (`300` celdas) y se pasó el guion `-` a nulo (`202` celdas) antes de usar `pd.to_numeric` para poder calcular medias y cuartiles.
   - En `horas_trabajo_semana` se cambiaron los `2822` guiones por nulo y se convirtió la columna a número.
   - En `distancia_km` se reemplazaron los `152` valores `999` por nulo (`NaN`) para que no inflaran las estadísticas (antes de esto el promedio de distancia salía en 32.2 km con desviación de 121 km).
2. **Unificación de categorías (`programa`, `jornada`, `genero`, `ciudad_procedencia`):**
   - Se aplicó `.str.strip().str.lower()` y luego un diccionario con `.replace()` para dejar únicamente los nombres de `VALIDOS`. Se corrigieron `260` filas en `programa`, `485` en `jornada`, `559` en `genero` y `542` en `ciudad_procedencia`. La categoría `Otra ciudad` se dejó tal cual porque agrupa municipios distintos y no es un error de escritura.
3. **Unificación de fechas (`fecha_matricula`):**
   - Se convirtieron por separado los formatos `%Y-%m-%d` y `%d/%m/%Y` con `errors="coerce"` y se unieron con `fillna()`, corrigiendo las `3052` fechas que venían en día/mes/año sin perder ninguna fila.
4. **Eliminación de duplicados:**
   - Se eliminaron las `150` filas repetidas con `drop_duplicates().reset_index(drop=True)`. Como tenían exactamente el mismo `id_estudiante` y los mismos valores en todas las columnas, conservarlas habría contado dos veces al mismo estudiante.
5. **Tratamiento de faltantes reales (`promedio_acumulado`, `ciudad_procedencia`, `tipo_colegio`):**
   - En `promedio_acumulado` se eliminaron las `298` filas con nulo usando `dropna(subset=["promedio_acumulado"])`. Una nota académica no se puede inventar, y rellenarla con la media o mediana le asignaría una nota ficticia a casi 300 estudiantes, alterando el análisis.
   - En `ciudad_procedencia` (`96` nulos restantes tras limpiar promedio) y `tipo_colegio` (`145` nulos restantes) se reemplazó el vacío por `'Sin dato'`, porque borrar esas filas haría perder datos académicos reales de esos estudiantes.
   - `motivo_retiro` se dejó con sus nulos porque en estudiantes activos y graduados no existe motivo de retiro.
6. **Tratamiento de valores imposibles (`promedio_acumulado`, `edad`, `horas_trabajo_semana`):**
   - En `promedio_acumulado` se eliminaron las `15` filas con valores mayores a 5 (`45`, `62` y `78`). Como advierte la guía, no se debe asumir sin certeza en qué escala estaban ni inventarles una nota.
   - En `edad`, los `12` casos de `12` y `150` años se pasaron a nulo y se reemplazaron por la mediana de edad (`22` años), ya que la mediana no se desajusta por valores extremos.
   - En `horas_trabajo_semana`, primero a los `2703` registros donde `trabaja == "no"` y las horas eran nulas se les puso `0` horas (si no trabaja, trabaja 0 horas). Después, los `29` casos con `200` horas se pasaron a nulo y se reemplazaron por la mediana calculada solo entre quienes sí trabajan (`24` horas).
   - Al comparar los boxplots en `distribuciones_antes_despues.png`, antes de limpiar las cajas casi ni se distinguían por culpa del 78 en promedio y el 150 en edad. Después de limpiar, se ve bien la distribución real (promedios entre 1.17 y 5.0 con mediana 3.68, y edades entre 17 y 29 años con mediana 22). Quedan algunos puntos sueltos fuera de los bigotes (notas bajas entre 1.17 y 1.88, y edades de 28 y 29 años), pero decidí dejarlos porque son valores completamente posibles en la vida real y no errores de digitación.

### 3. Respuestas a las cinco preguntas

Después de la limpieza, el dataset quedó con **`9687` estudiantes** (`3136` desertores, lo que representa una tasa general de deserción del `32.37 %`).

**Pregunta 1: ¿Qué programa presenta la tasa de deserción más alta?**
- **Ingeniería Industrial:** tasa de **`40.20 %`** (`0.4020`), con `1271` estudiantes.
- **Ingeniería de Sistemas:** tasa de `38.24 %` (`0.3824`), con `1386` estudiantes.
- **Diseño Gráfico:** tasa de `35.61 %` (`0.3561`), con `848` estudiantes.
- **Enfermería:** tasa de `31.27 %` (`0.3127`), con `1132` estudiantes.
- **Derecho:** tasa de `30.55 %` (`0.3055`), con `1447` estudiantes.
- **Administración de Empresas:** tasa de `29.68 %` (`0.2968`), con `1304` estudiantes.
- **Contaduría Pública:** tasa de `27.02 %` (`0.2702`), con `1162` estudiantes.
- **Psicología:** tasa de `26.03 %` (`0.2603`), con `1137` estudiantes.
- *Conclusión:* El programa con la deserción más alta es **Ingeniería Industrial** (`40.20 %` sobre `1271` estudiantes), seguido de cerca por Ingeniería de Sistemas (`38.24 %` sobre `1386` estudiantes). Todos los programas tienen grupos grandes (el menor es Diseño Gráfico con `848` estudiantes), por lo que las tasas son estables y no están distorsionadas por tamaños de muestra pequeños.

**Pregunta 2: ¿Hay diferencia en la deserción entre becados y no becados?**
- **Sin beca (`no`):** tasa de deserción de **`36.38 %`** (`0.3638`), con `7004` estudiantes.
- **Con beca (`sí`):** tasa de deserción de **`21.92 %`** (`0.2192`), con `2683` estudiantes.
- *Conclusión:* Sí hay una diferencia marcada de `14.46` puntos porcentuales: los estudiantes sin beca desertan bastante más (`36.38 %`) que los becados (`21.92 %`). Sin embargo, esa diferencia observada no prueba por sí sola que la beca sea la causa directa de que se queden, porque para obtener o mantener una beca muchas veces se exige buen promedio o mayor dedicación, factores que también reducen la deserción.

**Pregunta 3: ¿Qué jornada tiene el menor promedio acumulado?**
- **Nocturna:** promedio acumulado de **`3.46`** (`3.4644`), con `2666` estudiantes.
- **Fin de semana:** promedio acumulado de `3.70` (`3.7045`), con `949` estudiantes.
- **Diurna:** promedio acumulado de `3.72` (`3.7249`), con `6072` estudiantes.
- *Conclusión:* La jornada con el menor promedio acumulado es la **Nocturna** (`3.46` entre `2666` estudiantes), frente a `3.70` en Fin de semana y `3.72` en Diurna.

**Pregunta 4: ¿Cuántas materias reprobadas tienen en promedio los desertores frente a los activos?**
- **Activos:** promedio de **`0.62`** materias reprobadas (`0.6232`), con `5692` estudiantes.
- **Desertores:** promedio de **`3.07`** materias reprobadas (`3.0660`), con `3136` estudiantes.
- *(Se excluyeron los `859` graduados).*
- *Conclusión:* Los desertores tienen en promedio casi cinco veces más materias reprobadas (`3.07`) que los estudiantes activos (`0.62`). Es necesario excluir a los graduados porque ellos ya terminaron su carrera y no hacen parte de ninguno de los dos grupos que se quieren comparar (quienes siguen estudiando hoy frente a quienes abandonaron).

**Pregunta 5: ¿La deserción aumenta conforme baja la asistencia?**
- **Q1 (asistencia más baja, promedio `73.90 %`):** tasa de deserción de **`61.89 %`** (`0.6189`), con `2385` estudiantes.
- **Q2 (asistencia promedio `84.41 %`):** tasa de deserción de **`36.67 %`** (`0.3667`), con `2386` estudiantes.
- **Q3 (asistencia promedio `91.34 %`):** tasa de deserción de **`20.74 %`** (`0.2074`), con `2348` estudiantes.
- **Q4 (asistencia más alta, promedio `98.66 %`):** tasa de deserción de **`9.45 %`** (`0.0945`), con `2371` estudiantes.
- *(Nota: los cuartiles suman `9490` estudiantes porque `197` filas quedaron con asistencia nula al venir originalmente con `-`).*
- *Conclusión:* Sí, el patrón es muy claro: a medida que baja la asistencia, la deserción sube de forma constante, pasando de `9.45 %` en el cuartil de mayor asistencia (Q4) hasta `61.89 %` en el cuartil de menor asistencia (Q1). Aun así, esto no prueba que faltar a clase sea la causa original del retiro; muchas veces dejar de asistir es más bien un síntoma de que el estudiante ya tiene problemas económicos, laborales o de salud, o que ya decidió abandonar antes de que se registre formalmente la deserción.

### 4. Reflexión 1: asociación y causalidad

Aunque los datos muestran que la deserción entre los becados es menor (`21.92 %` frente a `36.38 %` en los no becados), eso solo demuestra una **asociación**, no que la beca cause directamente la permanencia. Puede haber otras variables detrás: por ejemplo, si la beca se entrega o se renueva según el rendimiento académico, quienes tienen beca podrían ser desde el principio estudiantes con mejores bases del colegio, mayor motivación o más tiempo para estudiar, y serían esas características (además del alivio económico) las que explican que no deserten. Para distinguir si la beca realmente causa la permanencia, habría que comparar estudiantes con condiciones académicas y socioeconómicas muy parecidas (por ejemplo, mismo promedio, estrato y jornada) o analizar un esquema donde el apoyo se asigne entre estudiantes con el mismo perfil de riesgo.

### 5. Reflexión 2: `motivo_retiro` y la predicción

La columna `motivo_retiro` **no se puede usar para predecir** la deserción antes de que ocurra, porque es un dato que solo se registra cuando el estudiante ya desertó (en el dataset todos los activos y graduados tienen ese campo vacío). Si se metiera en un modelo predictivo, el modelo haría trampa porque sabría que cualquiera con un motivo escrito es desertor al 100 %, pero en la vida real ese dato no existe cuando el estudiante todavía está activo y queremos prevenir que se retire.

Otras columnas del dataset que tienen el mismo problema o parecido son:
- `estado` y `desertor`, porque son justamente el resultado final.
- En parte también variables acumuladas como `semestre` o `creditos_aprobados` si se comparan sin cuidado contra los `graduados`, porque alguien con todos los créditos aprobados ya terminó; para alertas tempranas hay que comparar estudiantes en el mismo momento de su carrera.

### 6. Reflexión 3: uso de variables sensibles

Variables como `genero`, `estrato` o `ciudad_procedencia` reflejan condiciones sociales o demográficas que el estudiante no controla. Si la institución las usa de forma directa para decidir quién recibe o no recibe apoyo (por ejemplo, priorizar o descartar a alguien solo por su género o su ciudad), corre el riesgo de caer en discriminación y dejar por fuera a estudiantes de otros grupos que sí están en riesgo real de abandonar por bajas notas, inasistencia o dificultades económicas.

En lugar de usar el género o la ciudad como filtro para dar o negar ayudas individuales, es más justo y útil que la institución focalice los apoyos tempranos usando indicadores académicos y de seguimiento directo (como baja asistencia en `Q1`, materias reprobadas o bajo promedio acumulado), y que use variables como el `estrato` o la `distancia_km` únicamente para diseñar programas de bienestar general (como auxilios de transporte o becas socioeconómicas) sin estigmatizar a ningún grupo.

