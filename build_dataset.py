"""Construye el dataset final usado en la práctica.

Fuentes originales:
- https://www.kaggle.com/datasets/pinuto/global-energy-generation-and-capacity-imf
- https://www.kaggle.com/datasets/shahriarkabir/global-electricity-demand-and-generation-dataset

"""

from pathlib import Path

import pandas as pd

RENEWABLE_ENERGY_DATASET = Path(__file__).parent / "data" / "Renewable_Energy.csv"
ELECTRICITY_DEMAND_DATASET = (
    Path(__file__).parent
    / "data"
    / "Global_Electricity_Demandand_Generation_Dataset.csv"
)


def change_format(df: pd.DataFrame) -> pd.DataFrame:
    """Cambia el formato del dataset de demanda y generación de electricidad.

    Para que coincida con el formato del dataset de energía renovable, vamos
    a pivotar las variables 'Year' y 'Electricity demand - TWh'. Así, tendremos
    'Year' en columnas, que retendrán el valor de energía demandada en ese año.
    La variable 'Electricity generation - TWh' se eliminará, pues ya está en el
    otro dataset. También, cambiaremos la unidad de TWh a GWh.

    """
    # Cambiamos la unidad de TWh a GWh
    df["Electricity demand - TWh"] = df["Electricity demand - TWh"] * 1e3
    # Eliminamos la variable 'Electricity generation - TWh'
    df = df.drop(columns="Electricity generation - TWh")
    # Pivotamos las variables 'Year' y 'Electricity demand - TWh'
    df = df.pivot(
        index=["Entity", "Code"], columns="Year", values="Electricity demand - TWh"
    )
    df = df.rename(columns=lambda x: f"F{x}")
    df = df.reset_index()
    return df


def merge_datasets(
    df_renewable: pd.DataFrame, df_electricity_demand: pd.DataFrame
) -> pd.DataFrame:
    """Une los datasets de energía renovable y demanda de electricidad en uno
    solo.

    En concreto, el de electricidad demandada se unirá al de energías
    renovables, al tener este último más información.

    En primer lugar, toda fila del dataset de energías renovables cuyo país
    no aparezca en el de demanda de electricidad se eliminará. Se discriminará
    por las variables 'ISO3' y 'Code', respectivamente. También se eliminará
    la fila si el país no tiene código ISO3.

    Se añadirán las filas de un dataset al otro, con las siguientes variables:
     - Country: Valor de la columna 'Entity'
     - ISO3: Valor de la columna 'Code'
     - Indicator: "Electricity demand"
     - Technology: "Total"
     - Unit: "Gigawatt-hours (Gwh)"
     - F2000 -> F2022: Valores de las columnas 'F2000' a 'F2022'
    En todas las demás, NaN.

    Si existen códigos en el dataset de demanda de electricidad que no estén en
    el de energías renovables, se ignorarán.

    """
    # Renombramos las columnas del dataset de energía renovable
    df_electricity_demand = df_electricity_demand.rename(
        columns={"Entity": "Country", "Code": "ISO3"}
    )

    # Eliminamos las filas cuyo país no esté en el dataset de demanda de
    # electricidad
    df_renewable = df_renewable[
        df_renewable["ISO3"].isin(df_electricity_demand["ISO3"])
    ]

    # Añadimos las filas de un dataset al otro
    df = pd.concat(
        [
            df_renewable,
            df_electricity_demand.assign(
                Indicator="Electricity Demand",
                Technology="Total",
                Energy_Type="Any",
                Unit="Gigawatt-hours (Gwh)",
            ),
        ],
        ignore_index=True,
    )

    # Eliminamos toda fila cuyo país no tenga código ISO3
    df = df.dropna(subset=["ISO3"])

    return df


if __name__ == "__main__":
    # Cargamos los datasets
    df_renewable = pd.read_csv(RENEWABLE_ENERGY_DATASET)
    df_electricity_demand = pd.read_csv(ELECTRICITY_DEMAND_DATASET)

    # Cambiamos el formato del dataset de demanda y generación de electricidad
    df_electricity_demand = change_format(df_electricity_demand)

    # Unimos los datasets en uno solo
    df = merge_datasets(df_renewable, df_electricity_demand)

    # Nos deshacemos de todas las columnas inservibles
    unused_columns = [
        "ObjectId",
        "ISO2",
        "Source",
        "CTS_Name",
        "CTS_Code",
        "CTS_Full_Descriptor",
    ]
    df = df.drop(columns=unused_columns)

    # Y todas las de año que no estén en el rango [2000, 2022]
    df = df.drop(
        columns=[f"F{x}" for x in range(1990, 2024) if x not in range(2000, 2023)]
    )
    print(df.columns)

    # Guardamos el dataset final
    df.to_csv(Path(__file__).parent / "data" / "final_dataset.csv", index=False)
    print("Dataset final guardado en 'data/final_dataset.csv'")

    # Guardar también como Excel
    df.to_excel(Path(__file__).parent / "data" / "final_dataset.xlsx", index=False)
    print("Dataset final guardado en 'data/final_dataset.xlsx'")
