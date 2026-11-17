import pandas as pd


def _quitar_espacios(df):
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()
    return df


def limpiar_clientes(clientes):
    print("\n[clientes] Nulos por columna:")
    print(clientes.isnull().sum())
    print(f"[clientes] Filas duplicadas: {clientes.duplicated().sum()}")

    clientes = _quitar_espacios(clientes)

    # TODO 1: poner la columna "ciudad" en formato título (.str.title()).
    clientes["ciudad"] = clientes["ciudad"].str.title()

    # TODO 2: eliminar las filas duplicadas (.drop_duplicates()) y reiniciar el índice (.reset_index(drop=True)).
    clientes = clientes.drop_duplicates().reset_index(drop=True)

    print("\n[clientes] Nulos tras limpieza:")
    print(clientes.isnull().sum())
    print(f"[clientes] Filas duplicadas tras limpieza: {clientes.duplicated().sum()}")
    print(f"[clientes] Filas tras limpieza: {len(clientes)}")
    return clientes


def limpiar_ventas(ventas):
    print("\n[ventas] Nulos por columna:")
    print(ventas.isnull().sum())
    print(f"[ventas] Filas duplicadas: {ventas.duplicated().sum()}")

    ventas = _quitar_espacios(ventas)

    # TODO 3: rellenar los nulos de "producto" con el texto "Sin especificar" (.fillna()).
    #         Pista: no uses dropna(); estarías borrando una venta con dinero real.
    ventas["producto"] = ventas["producto"].fillna("Sin especificar")

    # TODO 4: convertir "fecha_venta" a fecha con pd.to_datetime().
    #         Pista: el formato de los datos es AAAA-MM-DD.
    ventas["fecha_venta"] = pd.to_datetime(ventas["fecha_venta"], format="%Y-%m-%d", errors="coerce")

    # TODO 5: eliminar las filas duplicadas y reiniciar el índice.
    ventas = ventas.drop_duplicates().reset_index(drop=True)

    print("\n[ventas] Nulos tras limpieza:")
    print(ventas.isnull().sum())
    print(f"[ventas] Filas duplicadas tras limpieza: {ventas.duplicated().sum()}")
    print(f"[ventas] Tipo de fecha_venta: {ventas['fecha_venta'].dtype}")
    print(f"[ventas] Filas tras limpieza: {len(ventas)}")
    return ventas


def limpiar_datos(clientes, ventas):
    return limpiar_clientes(clientes), limpiar_ventas(ventas)
