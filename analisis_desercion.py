from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

RAW = Path(__file__).parent / "Data" / "raw" / "datos_estudiantes.csv"
PROCESSED = Path(__file__).parent / "Data" / "processed"
GRAFICOS = PROCESSED / "graficos"

# Valores válidos de cada columna categórica (la forma correcta de escribirlos).
VALIDOS = {
    "programa": ["Administración de Empresas", "Contaduría Pública", "Derecho", "Psicología",
                 "Ingeniería de Sistemas", "Ingeniería Industrial", "Enfermería", "Diseño Gráfico"],
    "jornada": ["Diurna", "Nocturna", "Fin de semana"],
    "genero": ["Femenino", "Masculino"],
    "ciudad_procedencia": ["Bogotá", "Medellín", "Cali", "Bucaramanga", "Rionegro",
                           "Barranquilla", "Otra ciudad"],
}

DECISIONES = []


def registrar(paso, columna, accion, filas, justificacion):
    """Guarda una decisión para la tabla de decisiones. Ya está escrita: solo úsala."""
    DECISIONES.append({
        "paso": paso, "columna": columna, "accion": accion,
        "filas_afectadas": int(filas), "justificacion": justificacion,
    })


def explorar(df):
    """Paso 1 del Word: primera mirada al dataset.

    Muestra la forma, los tipos y los nulos de cada columna, las estadísticas
    numéricas, y los valores de las columnas programa, jornada, genero y estado.
    Pregunta: ¿alguna columna numérica aparece como texto? ¿Por qué crees que pasa?
    Respuesta: Sí, asistencia_pct y horas_trabajo_semana aparecen como str (texto)
    porque tienen caracteres como el símbolo '%' o guiones '-' para indicar faltantes.
    """
    print("=== Forma del dataset ===")
    print(df.shape)
    print("\n=== Tipos de datos y no nulos ===")
    df.info()
    print("\n=== Estadísticas numéricas ===")
    print(df.describe())

    for col in ["programa", "jornada", "genero", "ciudad_procedencia", "estado"]:
        print(f"\n=== Valores de {col} ===")
        print(df[col].value_counts())


def auditar(df):
    """Paso 2 del Word: buscar problemas sin corregirlos todavía.

    Revisa: nulos reales, faltantes disfrazados ('-', 999), valores imposibles
    (edad, promedio, horas), duplicados y formatos de fecha.
    Pregunta: ¿cuál de estos problemas afecta más el análisis? ¿Por qué?
    Respuesta: Los valores imposibles (como promedios de 62 o 78 y edades de 150) y las
    columnas numéricas en texto, porque distorsionan por completo los promedios o impiden
    hacer cálculos hasta que se limpien.
    """
    print("\n=== Auditoría de calidad ===")
    print("Nulos reales por columna:")
    print(df.isnull().sum())

    print("\nFaltantes disfrazados y símbolos:")
    print("Guiones en asistencia_pct:", (df["asistencia_pct"] == "-").sum())
    print("Celdas con '%' en asistencia_pct:", df["asistencia_pct"].str.contains("%", regex=False).sum())
    print("Guiones en horas_trabajo_semana:", (df["horas_trabajo_semana"] == "-").sum())
    print("Valores 999 en distancia_km:", (df["distancia_km"] == 999).sum())

    print("\nDuplicados exactos:", df.duplicated().sum())

    horas_temp = pd.to_numeric(df["horas_trabajo_semana"].replace("-", np.nan), errors="coerce")
    print("\nValores imposibles:")
    print("Edad fuera de 15 a 60:", ((df["edad"] < 15) | (df["edad"] > 60)).sum())
    print("Promedio acumulado mayor a 5:", (df["promedio_acumulado"] > 5).sum())
    print("Horas de trabajo mayores a 100:", (horas_temp > 100).sum())

    iso = pd.to_datetime(df["fecha_matricula"], format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(df["fecha_matricula"], format="%d/%m/%Y", errors="coerce")
    print("\nFormatos de fecha:")
    print("Formato AAAA-MM-DD:", iso.notnull().sum())
    print("Formato DD/MM/AAAA:", dmy.notnull().sum())


def convertir_numericos(df):
    """Paso 3 del Word: columnas que deberían ser numéricas, pero llegan como texto.

    Pistas: quitar el símbolo % con str.replace; reemplazar '-' por nulo;
    convertir con pd.to_numeric(..., errors="coerce"); reemplazar 999 por nulo en distancia_km.
    Registra cada conversión con registrar().
    """
    con_porcentaje = df["asistencia_pct"].str.contains("%", regex=False).sum()
    guiones_asistencia = (df["asistencia_pct"] == "-").sum()
    df["asistencia_pct"] = df["asistencia_pct"].str.replace("%", "", regex=False)
    df["asistencia_pct"] = pd.to_numeric(df["asistencia_pct"].replace("-", np.nan), errors="coerce")
    registrar(
        "convertir_numericos", "asistencia_pct", "quitar % y pasar '-' a nulo",
        con_porcentaje + guiones_asistencia,
        "Tenía 300 valores con '%' y 202 con '-' que impedían calcular promedios y cuartiles."
    )

    guiones_horas = (df["horas_trabajo_semana"] == "-").sum()
    df["horas_trabajo_semana"] = pd.to_numeric(
        df["horas_trabajo_semana"].replace("-", np.nan), errors="coerce"
    )
    registrar(
        "convertir_numericos", "horas_trabajo_semana", "reemplazar '-' por nulo y convertir a número",
        guiones_horas,
        "El guion representaba un faltante disfrazado en texto para estudiantes que no trabajan."
    )

    codigos_999 = (df["distancia_km"] == 999).sum()
    df["distancia_km"] = df["distancia_km"].replace(999, np.nan)
    registrar(
        "convertir_numericos", "distancia_km", "reemplazar 999 por nulo",
        codigos_999,
        "999 no es una distancia real sino un código para indicar que no había dato."
    )
    return df


def unificar_categorias(df):
    """Paso 4 del Word: errores tipográficos en columnas categóricas.

    Pistas: primero df[col].str.strip().str.lower(); después .replace(diccionario)
    con las variantes que encontraste con value_counts(). Los valores correctos están en VALIDOS.
    Pregunta: ¿qué variantes son el mismo valor? ¿Hay alguna que no debas unificar?
    Respuesta: Son el mismo valor las diferencias por mayúsculas, espacios al final, tildes
    faltantes (psicologia, ingenieria, bogota, medellin) e iniciales (f/m). No se debe unificar
    'Otra ciudad' con ninguna ciudad específica porque agrupa orígenes distintos.
    """
    mapas = {
        "programa": {
            "administración de empresas": "Administración de Empresas",
            "contaduría pública": "Contaduría Pública",
            "derecho": "Derecho",
            "psicología": "Psicología",
            "psicologia": "Psicología",
            "ingeniería de sistemas": "Ingeniería de Sistemas",
            "ingenieria de sistemas": "Ingeniería de Sistemas",
            "ingeniería industrial": "Ingeniería Industrial",
            "enfermería": "Enfermería",
            "diseño gráfico": "Diseño Gráfico",
        },
        "jornada": {
            "diurna": "Diurna",
            "nocturna": "Nocturna",
            "fin de semana": "Fin de semana",
        },
        "genero": {
            "femenino": "Femenino",
            "f": "Femenino",
            "masculino": "Masculino",
            "m": "Masculino",
        },
        "ciudad_procedencia": {
            "bogotá": "Bogotá",
            "bogota": "Bogotá",
            "medellín": "Medellín",
            "medellin": "Medellín",
            "cali": "Cali",
            "bucaramanga": "Bucaramanga",
            "rionegro": "Rionegro",
            "barranquilla": "Barranquilla",
            "otra ciudad": "Otra ciudad",
        },
    }

    for col, diccionario in mapas.items():
        antes = df[col].copy()
        df[col] = df[col].str.strip().str.lower().replace(diccionario)
        cambiadas = ((antes != df[col]) & antes.notnull()).sum()
        registrar(
            "unificar_categorias", col, "normalizar texto y unificar variantes",
            cambiadas,
            f"Había variantes por mayúsculas, espacios o tildes que separaban una misma categoría en {col}."
        )
    return df


def convertir_fechas(df):
    """Paso 5 del Word: fechas escritas en dos formatos.

    Pista: intenta el formato AAAA-MM-DD y luego DD/MM/AAAA, cada uno con errors="coerce",
    y junta los resultados con fillna(). Registra cuántas fechas tenían el segundo formato.
    """
    iso = pd.to_datetime(df["fecha_matricula"], format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(df["fecha_matricula"], format="%d/%m/%Y", errors="coerce")
    en_dmy = dmy.notnull().sum()
    df["fecha_matricula"] = iso.fillna(dmy)
    registrar(
        "convertir_fechas", "fecha_matricula", "unificar formatos AAAA-MM-DD y DD/MM/AAAA",
        en_dmy,
        "Las fechas venían mezcladas en dos formatos y se requería un tipo datetime uniforme."
    )
    return df


def eliminar_duplicados(df):
    """Paso 6 del Word: filas repetidas.

    Pregunta: ¿podrían existir dos estudiantes distintos con todos los datos iguales?
    Pista: duplicated() y drop_duplicates(), con reset_index(drop=True).
    Respuesta: No, porque la columna id_estudiante es un identificador único por persona;
    si hasta el id_estudiante se repite, es un registro duplicado por error.
    """
    duplicadas = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    registrar(
        "eliminar_duplicados", "todas", "eliminar filas duplicadas",
        duplicadas,
        "Eran registros repetidos con el mismo id_estudiante que inflaban los conteos."
    )
    return df


def tratar_faltantes(df):
    """Paso 7 del Word: decidir qué hacer con los nulos reales.

    Preguntas:
    - ¿Puedes inventar una nota? ¿Qué pasa si imputas el promedio?
    - Para ciudad o tipo de colegio, ¿conviene eliminar la fila o marcar el dato como 'Sin dato'?
    - motivo_retiro tiene muchos nulos. ¿Son errores? (Pista: ¿para quiénes aplica esa columna?)
    Respuesta:
    - No se puede inventar una nota; imputar el promedio metería ruido en una variable clave.
    - En ciudad_procedencia y tipo_colegio conviene usar 'Sin dato' para no perder el resto de la fila.
    - Los nulos de motivo_retiro no son errores: solo aplica a quienes desertaron, por lo que en
      activos y graduados es normal que esté vacío.
    """
    nulos_promedio = df["promedio_acumulado"].isnull().sum()
    df = df.dropna(subset=["promedio_acumulado"]).reset_index(drop=True)
    registrar(
        "tratar_faltantes", "promedio_acumulado", "eliminar filas",
        nulos_promedio,
        "Una nota académica no se puede inventar sin distorsionar el análisis de rendimiento."
    )

    nulos_ciudad = df["ciudad_procedencia"].isnull().sum()
    df["ciudad_procedencia"] = df["ciudad_procedencia"].fillna("Sin dato")
    registrar(
        "tratar_faltantes", "ciudad_procedencia", "reemplazar nulos por 'Sin dato'",
        nulos_ciudad,
        "Permite conservar la información académica del estudiante sin inventar su ciudad."
    )

    nulos_colegio = df["tipo_colegio"].isnull().sum()
    df["tipo_colegio"] = df["tipo_colegio"].fillna("Sin dato")
    registrar(
        "tratar_faltantes", "tipo_colegio", "reemplazar nulos por 'Sin dato'",
        nulos_colegio,
        "Se conserva el estudiante en el análisis marcando explícitamente que falta ese dato."
    )
    return df


def tratar_imposibles(df):
    """Paso 8 del Word: valores que no pueden existir.

    Preguntas:
    - La escala del promedio es de 0 a 5. ¿Qué harías con un 45?
    - Una edad de 150 años es un error. ¿Qué valor pondrías en su lugar?
    - Si el estudiante no trabaja, ¿cuántas horas de trabajo tiene? ¿Cómo lo aplicas en código?
    Respuesta:
    - Un promedio mayor a 5 (hay valores de 45, 62 y 78) es imposible en escala 0 a 5 y no se
      puede adivinar la escala real ni inventar la nota, así que se eliminan esas filas.
    - Una edad de 150 (o de 12) se pasa a nulo y se reemplaza por la mediana de edad.
    - Si no trabaja, tiene 0 horas; se asigna con df.loc[(df["trabaja"] == "no") & df["horas_trabajo_semana"].isnull(), "horas_trabajo_semana"] = 0.
    """
    prom_imposibles = (df["promedio_acumulado"] > 5).sum()
    df = df[df["promedio_acumulado"] <= 5].reset_index(drop=True)
    registrar(
        "tratar_imposibles", "promedio_acumulado", "eliminar filas con promedio > 5",
        prom_imposibles,
        "Valores como 45, 62 y 78 están fuera de la escala de 0 a 5 y una nota no se debe inventar."
    )

    edades_imposibles = ((df["edad"] < 15) | (df["edad"] > 60)).sum()
    df.loc[(df["edad"] < 15) | (df["edad"] > 60), "edad"] = np.nan
    mediana_edad = df["edad"].median()
    df["edad"] = df["edad"].fillna(mediana_edad)
    registrar(
        "tratar_imposibles", "edad", f"reemplazar edades fuera de 15-60 por la mediana ({mediana_edad:.0f})",
        edades_imposibles,
        "Edades de 12 y 150 años son errores de registro; se usa la mediana porque no la afectan los extremos."
    )

    no_trabaja_nulos = ((df["trabaja"] == "no") & df["horas_trabajo_semana"].isnull()).sum()
    df.loc[(df["trabaja"] == "no") & df["horas_trabajo_semana"].isnull(), "horas_trabajo_semana"] = 0
    registrar(
        "tratar_imposibles", "horas_trabajo_semana", "asignar 0 horas cuando trabaja es 'no'",
        no_trabaja_nulos,
        "Si el estudiante reporta que no trabaja, sus horas trabajadas por semana son 0."
    )

    horas_imposibles = (df["horas_trabajo_semana"] > 100).sum()
    df.loc[df["horas_trabajo_semana"] > 100, "horas_trabajo_semana"] = np.nan
    mediana_trabajadores = df.loc[df["trabaja"] == "sí", "horas_trabajo_semana"].median()
    df["horas_trabajo_semana"] = df["horas_trabajo_semana"].fillna(mediana_trabajadores)
    registrar(
        "tratar_imposibles", "horas_trabajo_semana",
        f"reemplazar valores > 100 por la mediana de quienes trabajan ({mediana_trabajadores:.0f})",
        horas_imposibles,
        "200 horas supera las 168 horas de una semana; se reemplaza con la mediana de los que sí trabajan."
    )
    return df


def crear_variables(df):
    """Paso 9 del Word: variables nuevas para el análisis.

    Crea:
    - desertor: True si estado es 'desertor', False si no.
    - cuartil_asistencia: divide asistencia_pct en cuatro grupos iguales con pd.qcut.
    Pregunta: ¿por qué conviene usar cuartiles y no valores exactos de asistencia?
    Respuesta: Porque con decimales exactos habría demasiados valores distintos con pocos
    estudiantes cada uno; agrupar en cuatro bloques de tamaño similar permite ver la tendencia.
    """
    df["desertor"] = df["estado"].eq("desertor")
    df["cuartil_asistencia"] = pd.qcut(df["asistencia_pct"], 4, labels=["Q1", "Q2", "Q3", "Q4"])
    print(f"\nTotal de desertores: {df['desertor'].sum()} de {len(df)} estudiantes.")
    return df


def grafico_faltantes(df):
    """Gráfico 1: mapa de faltantes del dataset original.

    Pista: sns.heatmap(df.isnull(), cbar=False)
    """
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Mapa de valores faltantes (dataset original)")
    plt.savefig(GRAFICOS / "mapa_faltantes.png", bbox_inches="tight")
    plt.show()
    plt.close()


def grafico_distribuciones(antes, despues):
    """Gráfico 2: boxplots de promedio_acumulado y edad, antes y después de limpiar.

    Pregunta: ¿qué cambió en cada distribución? ¿Por qué?
    Respuesta: Antes de limpiar, las cajas casi no se veían porque los valores extremos
    (promedios hasta 78 y edades de 150) estiraban toda la escala. Después de limpiar, se
    aprecia bien el rango real de notas (0 a 5) y de edades (17 a 29 años).
    """
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    fig, ejes = plt.subplots(2, 2, figsize=(12, 8))

    sns.boxplot(x=antes["promedio_acumulado"], ax=ejes[0, 0])
    ejes[0, 0].set_title("promedio_acumulado (antes)")

    sns.boxplot(x=despues["promedio_acumulado"], ax=ejes[0, 1])
    ejes[0, 1].set_title("promedio_acumulado (después)")

    sns.boxplot(x=antes["edad"], ax=ejes[1, 0])
    ejes[1, 0].set_title("edad (antes)")

    sns.boxplot(x=despues["edad"], ax=ejes[1, 1])
    ejes[1, 1].set_title("edad (después)")

    plt.tight_layout()
    plt.savefig(GRAFICOS / "distribuciones_antes_despues.png", bbox_inches="tight")
    plt.show()
    plt.close()


def grafico_tasa_programa(df):
    """Gráfico 3: tasa de deserción por programa.

    Pista: df.groupby("programa")["desertor"].mean()
    """
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    tasa = df.groupby("programa")["desertor"].mean().sort_values(ascending=False)
    tasa.plot(kind="bar")
    plt.title("Tasa de deserción por programa")
    plt.ylabel("Proporción de desertores")
    plt.savefig(GRAFICOS / "tasa_desercion_por_programa.png", bbox_inches="tight")
    plt.show()
    plt.close()


def grafico_tasa_asistencia(df):
    """Gráfico 4: tasa de deserción por cuartil de asistencia.

    Pista: df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()
    """
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    tasa = df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()
    tasa.plot(kind="bar")
    plt.title("Tasa de deserción por cuartil de asistencia")
    plt.ylabel("Proporción de desertores")
    plt.savefig(GRAFICOS / "tasa_desercion_por_asistencia.png", bbox_inches="tight")
    plt.show()
    plt.close()


def responder_preguntas(df):
    """Paso 10 del Word: las cinco preguntas de la institución.

    Cada pregunta debe imprimir el resultado con el número de estudiantes por grupo.
    Pregunta 1: ¿Qué programa presenta la tasa de deserción más alta?
    Pregunta 2: ¿Hay diferencia en la deserción entre becados y no becados?
    Pregunta 3: ¿Qué jornada tiene el menor promedio acumulado?
    Pregunta 4: ¿Cuántas materias reprobadas tienen en promedio los desertores frente a los activos?
                (Excluye a los graduados.)
    Pregunta 5: ¿La deserción aumenta conforme baja la asistencia?
                (Usa cuartil_asistencia.)
    """
    print("\n=== Pregunta 1: Tasa de deserción por programa ===")
    p1 = df.groupby("programa").agg(
        tasa=("desertor", "mean"),
        estudiantes=("desertor", "size")
    ).sort_values("tasa", ascending=False)
    print(p1)

    print("\n=== Pregunta 2: Deserción entre becados y no becados ===")
    p2 = df.groupby("beca").agg(
        tasa=("desertor", "mean"),
        estudiantes=("desertor", "size")
    )
    print(p2)

    print("\n=== Pregunta 3: Promedio acumulado por jornada ===")
    p3 = df.groupby("jornada").agg(
        promedio=("promedio_acumulado", "mean"),
        estudiantes=("promedio_acumulado", "size")
    ).sort_values("promedio")
    print(p3)

    print("\n=== Pregunta 4: Materias reprobadas (desertores vs activos, sin graduados) ===")
    sin_graduados = df[df["estado"] != "graduado"]
    p4 = sin_graduados.groupby("estado").agg(
        promedio_reprobadas=("materias_reprobadas", "mean"),
        estudiantes=("materias_reprobadas", "size")
    )
    print(p4)

    print("\n=== Pregunta 5: Deserción por cuartil de asistencia ===")
    p5 = df.groupby("cuartil_asistencia", observed=True).agg(
        tasa=("desertor", "mean"),
        asistencia_promedio=("asistencia_pct", "mean"),
        estudiantes=("desertor", "size")
    )
    print(p5)


def guardar(df):
    """Paso 11 del Word: guardar el dataset limpio y la tabla de decisiones. Ya está escrito."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "dataset_limpio.csv", index=False)
    pd.DataFrame(DECISIONES).to_csv(PROCESSED / "decisiones.csv", index=False)
    print(f"\nDataset limpio guardado: {df.shape[0]} filas, {df.shape[1]} columnas.")


def main():
    original = pd.read_csv(RAW)
    df = original.copy()

    explorar(df)
    auditar(df)
    grafico_faltantes(df)

    df = convertir_numericos(df)
    df = unificar_categorias(df)
    df = convertir_fechas(df)
    df = eliminar_duplicados(df)
    df = tratar_faltantes(df)
    df = tratar_imposibles(df)
    df = crear_variables(df)

    grafico_distribuciones(original, df)
    grafico_tasa_programa(df)
    grafico_tasa_asistencia(df)

    responder_preguntas(df)
    print("\nTabla de decisiones:")
    print(pd.DataFrame(DECISIONES))
    guardar(df)


if __name__ == "__main__":
    main()
