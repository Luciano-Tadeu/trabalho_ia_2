import numpy as np
import pandas as pd

def celsius(f):
    return (f - 32) * 5/9

def m_2(pes):
    return pes * 0.0929

csv_path: str = "dados/recs2020_public_v7.csv"
colunas: dict[str, str] = {
    # Consumo:
    "KWH": "kWh",
    "NHSLDMEM": "moradores",
    # Temperatura:
    "HDD65": "graus-dia de frio (65 °F) em 2020",
    "CDD65": "graus-dia de calor (65 °F) em 2020",
    "TEMPHOME": "Temperatura no inverno, de dia, com gente em casa (°F)",
    "TEMPNITE": "Temperatura no inverno, à noite (°F)",
    # A Casa:
    "TOTROOMS": "total de cômodos, sem contar banheiros",
    "SQFTEST": "área da casa (pés^2)",
    # Número de Aparelhos:
    "NUMCFAN": "ventiladores de teto",
    "TVCOLOR": "TVs",
    "NUMFRIG": "geladeiras",
    "NUMFREEZ": "freezers separados",
    "MICRO": "micro-ondas",
    # Tem Aparelhos (1 sim, 0 não):
    "DISHWASH": "lava-louça",
    "CWASHER": "máquina de lavar roupa",
    "DRYER": "secadora de roupa",
}

# print(list(colunas))

df = pd.read_csv(csv_path)
df = df[list(colunas)]
df = df.replace(-2, np.nan).dropna() # Remover as linhas sem temperatura

df["TEMPNITE"] = celsius(df["TEMPNITE"])
df["TEMPHOME"] = celsius(df["TEMPHOME"])

df["SQFTEST"] = df["SQFTEST"] * 0.0929

print(df)
print(df.isnull().sum())

df.to_csv("dados/dados_pre_processado.csv",index=False)
