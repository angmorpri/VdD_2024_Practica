"""Construye los subconjuntos del dataset final para realizar las
visualizaciones específicas.

"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data"
CHARTS_PATH = DATA_PATH / "charts"
FINAL_DATASET = DATA_PATH / "final_dataset.csv"


def build_sunburst(df: pd.DataFrame) -> None:
    """Genera un dataset para la visualización de un diagrama de sol.

    Debe incluirse sólo donde 'Indicator' == 'Electricity Generation'.
    La primera columna debe ser 'Energy_Type', la segunda 'Technology', y la
    tercera, 'Value', la suma de todos los valores (de todos los países) para
    dicho tipo de energía y tecnología, por cada año ('F2000' a 'F2022').

    """
    df = df.copy()
    df = df[df["Indicator"] == "Electricity Installed Capacity"]
    df = df.groupby(["Energy_Type", "Technology"]).sum()
    df = df.drop(columns=["Country", "ISO3"])
    df = df.reset_index()
    df.to_excel(CHARTS_PATH / "sunburst2.xlsx", index=False)
    print("Hecho -> sunburst2.xlsx")


def build_rel_capacity_installed(df: pd.DataFrame) -> None:
    """Genera un dataset para la visualización de la capacidad instalada.

    Debe presentar la capacidad instalada de todo el mundo ('Indicator' =
    'Electricity Installed Capacity') por cada año ('F2000' a 'F2022'),
    agrupando por 'Energy_Type' y 'Technology'.

    """
    df = df.copy()
    df = df[df["Indicator"] == "Electricity Installed Capacity"]
    df = df.drop(columns=["Country", "ISO3"])
    df = df.groupby(["Energy_Type", "Technology"]).sum()
    df = df.reset_index()
    df.to_excel(CHARTS_PATH / "rel_capacity_installed.xlsx", index=False)
    print("Hecho -> rel_capacity_installed.xlsx")


def build_generation_vs_demand(df: pd.DataFrame) -> None:
    """Genera un dataset para la visualización de la generación vs. la demanda.

    Debe contener la generación de todo el mundo ('Indicator' = 'Electricity
    Generation') y la demanda ('Indicator' = 'Electricity Demand'), en total
    para todo el mundo, por cada año ('F2000' a 'F2022').

    """
    df = df.copy()
    df = df[
        (df["Indicator"] == "Electricity Generation")
        | (df["Indicator"] == "Electricity Demand")
    ]
    df = df.drop(columns=["Country", "ISO3"])
    df = df.groupby(["Indicator"]).sum()
    df = df.reset_index()
    df.to_excel(CHARTS_PATH / "generation_vs_demand.xlsx", index=False)
    print("Hecho -> generation_vs_demand.xlsx")


def build_world_diff(df: pd.DataFrame) -> None:
    """Dataset para visualizar por país la desviación de la generación fósil
    VS la generación renovable.

    Agrupando por país ('Country'), se debe calcular la diferencia entre
    'Energy_Type' == 'Non-Renewable' y la suma de todos los valores con
    'Energy_Type' == 'Renewable' para ese país, y dividirlo por la suma de
    ambos valores. El resultado debe ser una columna 'World_Diff'. Se debe
    hacer para cada año ('F2000' a 'F2022').

    """
    df = df.copy()
    df = df[df["Indicator"] == "Electricity Generation"]
    df = df.drop(columns=["ISO3", "Indicator", "Technology", "Unit"])
    df = df.groupby(["Country", "Energy_Type"]).sum()
    df = df.reset_index()

    df = df.melt(
        id_vars=["Country", "Energy_Type"],
        value_vars=["F2002", "F2012", "F2022"],
        var_name="Year",
        value_name="Value",
    )
    df = df.pivot(
        index=["Country", "Year"], columns="Energy_Type", values="Value"
    ).reset_index()
    df["Diff"] = -0.5 + (
        df["Total Non-Renewable"] / (df["Total Non-Renewable"] + df["Total Renewable"])
    )
    df = df[["Country", "Year", "Diff"]]

    df.to_excel(CHARTS_PATH / "world_diff.xlsx", index=False)
    print("Hecho -> world_diff.xlsx")


def build_most_expensive_countries(df: pd.DataFrame) -> None:
    """Dataset para visualizar los países con mayor demanda de energía,
    y generación renovable y no renovable, en los últimos 10 años.

    Se debe agrupar por países ('Country') y, para cada variable objetivo,
    sumar los últimos diez años ('F2013' a 'F2022'). Las columnas deberán ser
    'Country', 'Demand', 'Renewable', 'Non-Renewable'.

    """
    df = df.copy()
    df = df[df["Indicator"].isin(["Electricity Demand", "Electricity Generation"])]
    df = df.drop(columns=["Technology", "Unit"])
    df = df.groupby(["ISO3", "Energy_Type"]).sum()
    df = df.reset_index()

    sum_cols = ["F{}".format(i) for i in range(2013, 2023)]
    df["Total10"] = df[sum_cols].sum(axis=1)
    df = df.pivot(index="ISO3", columns="Energy_Type", values="Total10")

    df.to_excel(CHARTS_PATH / "most_expensive_countries.xlsx", index=True)
    print("Hecho -> most_expensive_countries.xlsx")


def build_renewable_generation_countries(df: pd.DataFrame) -> None:
    """Dataset para visualizar el crecimiento de la capacidad instalada
    renovable VS la no renovable por país en los últimos 10 años.

    """
    df = df.copy()
    df = df[df["Indicator"] == "Electricity Installed Capacity"]
    df = df.drop(columns=["Technology", "Unit"])
    df = df.groupby(["ISO3", "Energy_Type"]).sum()
    df = df.reset_index()
    df["RelDiff"] = df["F2022"] / df["F2013"]
    df = df.pivot(index="ISO3", columns="Energy_Type", values="RelDiff")

    df.to_excel(CHARTS_PATH / "renewable_generation_countries.xlsx", index=True)
    print("Hecho -> renewable_generation_countries.xlsx")


def build_renewable_vs_non_renewable(df: pd.DataFrame) -> None:
    """Dataset para visualizar el crecimiento de la energía generada por
    tecnología renovable VS por cada año, para el total de países.

    """
    df = df.copy()
    df = df[df["Indicator"] == "Electricity Generation"]
    df = df.drop(columns=["Country", "ISO3", "Technology", "Unit"])
    df = df.groupby(["Energy_Type"]).sum()
    df = df.reset_index()
    df.to_excel(CHARTS_PATH / "renewable_vs_non_renewable.xlsx", index=False)
    print("Hecho -> renewable_vs_non_renewable.xlsx")


def build_rel_growth(df: pd.DataFrame) -> None:
    """Dataset para visualizar el crecimiento relativo año a año de todas
    los campos estudiados.

    Luego, filtramos por energía generada, y agrupamos por tecnología renovable
    o no renovable.

    """
    # Relativo
    df = df.copy()
    for year in range(2001, 2023):
        df[f"R{year}"] = df[f"F{year}"] - df[f"F{year-1}"]

    # Agrupación
    df = df[df["Indicator"] == "Electricity Generation"]
    df = df.drop(columns=["Country", "ISO3", "Technology", "Unit"])
    df = df.groupby(["Energy_Type"]).sum()
    df = df.reset_index()
    df.to_excel(CHARTS_PATH / "rel_growth.xlsx", index=False)
    print("Hecho -> rel_growth.xlsx")


def build_rel_growth_2(df: pd.DataFrame) -> None:
    """Dataset para visualizar el crecimiento relativo año a año de todas
    los campos estudiados.

    Luego, filtramos por energía generada, y agrupamos por tecnología renovable
    o no renovable.

    """
    # Agrupación
    df = df[df["Indicator"] == "Electricity Generation"]
    df = df.drop(columns=["Country", "ISO3", "Technology", "Unit"])
    df = df.groupby(["Energy_Type"]).sum()
    df = df.reset_index()

    # Relativo
    for year in range(2001, 2023):
        df[f"R{year}"] = (df[f"F{year}"] / df[f"F{year-1}"]) - 1
    df = df.drop(columns=[f"F{year}" for year in range(2000, 2023)])
    df.to_excel(CHARTS_PATH / "rel_growth2.xlsx", index=False)
    print("Hecho -> rel_growth2.xlsx")


if __name__ == "__main__":
    df = pd.read_csv(FINAL_DATASET)

    build_rel_growth_2(df)
