import numpy as np
import pandas as pd


def celsius(f):
    return (f - 32) * 5 / 9


def m_2(pes):
    return pes * 0.0929


def outliers_kwh(df: pd.DataFrame):
    Q1 = df["kwh"].quantile(0.25)
    Q3 = df["kwh"].quantile(0.75)
    IQR = Q3 - Q1

    limite_cima = Q3 + 1.5 * IQR
    limite_baixo = Q1 - 1.5 * IQR

    return df[(df["kwh"] >= limite_baixo) & (df["kwh"] <= limite_cima)]


csv_path: str = "dados/recs2020_public_v7.csv"
colunas = {
    # Consumo:
    "KWH": {"nome_coluna": "kwh", "info": "kWh (quilowatt-hora)"},
    "NHSLDMEM": {"nome_coluna": "moradores", "info": "Número de moradores"},
    # Temperatura:
    "HDD65": {
        "nome_coluna": "graus_dia_frio_f",
        "info": "Graus-dia de frio (65 °F) em 2020",
    },
    "CDD65": {
        "nome_coluna": "graus_dia_calor_f",
        "info": "Graus-dia de calor (65 °F) em 2020",
    },
    "TEMPHOME": {
        "nome_coluna": "temp_inverno_dia_c",
        "info": "Temperatura no inverno, de dia, com gente em casa (°C)",
    },
    "TEMPNITE": {
        "nome_coluna": "temp_inverno_noite_c",
        "info": "Temperatura no inverno, à noite (°C)",
    },
    # A Casa:
    "TOTROOMS": {
        "nome_coluna": "total_comodos",
        "info": "Total de cômodos, sem contar banheiros",
    },
    "SQFTEST": {"nome_coluna": "area_casa_m2", "info": "Área da casa (m²)"},
    # Número de Aparelhos:
    "NUMCFAN": {"nome_coluna": "ventiladores_teto", "info": "Ventiladores de teto"},
    "TVCOLOR": {"nome_coluna": "tvs", "info": "TVs"},
    "NUMFRIG": {"nome_coluna": "geladeiras", "info": "Geladeiras"},
    "NUMFREEZ": {"nome_coluna": "freezers", "info": "Freezers separados"},
    "MICRO": {"nome_coluna": "microondas", "info": "Micro-ondas"},
    # Tem Aparelhos (1 sim, 0 não):
    "DISHWASH": {"nome_coluna": "lava_louca", "info": "Lava-louça"},
    "CWASHER": {"nome_coluna": "maquina_lavar", "info": "Máquina de lavar roupa"},
    "DRYER": {"nome_coluna": "secadora", "info": "Secadora de roupa"},
}

df = pd.read_csv(csv_path)
df = df[list(colunas)]
df = df.replace(-2, np.nan).dropna()  # Remover as linhas sem temperatura

df = df.rename(columns={k: v["nome_coluna"] for k, v in colunas.items()})

df["temp_inverno_noite_c"] = celsius(df["temp_inverno_noite_c"])
df["temp_inverno_dia_c"] = celsius(df["temp_inverno_dia_c"])

df["area_casa_m2"] = m_2(df["area_casa_m2"])

df = outliers_kwh(df)

print(df)

pd.DataFrame(colunas.values()).to_csv("dados/colunas.csv", index=False)
df.to_csv("dados/dados_pre_processado.csv", index=False)
