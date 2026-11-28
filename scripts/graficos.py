"""
Geração de gráficos para o projeto de regressão linear múltipla.

Estrutura esperada do projeto:
    raiz/
    ├── scripts/
    │   ├── graficos.py
    │   └── regressao_linear.py
    ├── dados/
    │   └── dados_pre_processado.csv
    └── graficos/  (criada automaticamente)

Execução:
    python graficos.py

Os gráficos são salvos em ../graficos, na raiz do projeto.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from regressao_linear import treinar_modelo


PASTA_RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_DADOS = PASTA_RAIZ / "dados" / "dados_pre_processado.csv"
PASTA_GRAFICOS = PASTA_RAIZ / "graficos"
ALVO = "kwh"

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11
DPI = 150


def salvar_grafico(nome):
    """Salva a figura atual e fecha para liberar memória."""
    caminho = PASTA_GRAFICOS / nome
    plt.tight_layout()
    plt.savefig(caminho, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Gráfico salvo: {caminho}")


def grafico_correlacao(df):
    """Matriz de correlação entre todas as colunas."""
    correlacao = df.corr(numeric_only=True)
    mascara = np.triu(np.ones_like(correlacao, dtype=bool))

    plt.figure(figsize=(15, 12))
    sns.heatmap(
        correlacao,
        mask=mascara,
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 7},
        linewidths=0.4,
        square=True,
        cbar_kws={"label": "Correlação"},
    )
    plt.title("Matriz de correlação das variáveis")
    salvar_grafico("01_matriz_correlacao.png")

    print("\nCorrelação de cada variável com kwh:")
    print(correlacao[ALVO].drop(ALVO).sort_values(ascending=False).to_string())


def graficos_dispersao(df):
    """Dispersão de cada variável independente contra kwh, em uma única imagem."""
    variaveis = [coluna for coluna in df.columns if coluna != ALVO]

    colunas_grade = 3
    linhas_grade = int(np.ceil(len(variaveis) / colunas_grade))

    fig, eixos = plt.subplots(
        linhas_grade,
        colunas_grade,
        figsize=(18, linhas_grade * 4.5),
    )
    eixos = np.array(eixos).flatten()

    # Amostra apenas para deixar a visualização mais leve.
    dados_plot = df.sample(n=min(5000, len(df)), random_state=42)

    for ax, coluna in zip(eixos, variaveis):
        sns.regplot(
            data=dados_plot,
            x=coluna,
            y=ALVO,
            ax=ax,
            ci=None,
            scatter_kws={"alpha": 0.25, "s": 12},
            line_kws={"linewidth": 2},
            color="steelblue",
        )
        ax.set_title(f"{coluna} × kwh")
        ax.set_xlabel(coluna)
        ax.set_ylabel("Consumo (kWh)")

    for ax in eixos[len(variaveis):]:
        fig.delaxes(ax)

    fig.suptitle(
        "Relação entre cada variável independente e o consumo de energia",
        fontsize=16,
        y=1.01,
    )
    salvar_grafico("02_dispersao_variaveis_kwh.png")


def grafico_real_vs_previsto(resultado):
    """Compara os valores reais e previstos no conjunto de teste."""
    y_real = np.asarray(resultado["y_test"])
    y_previsto = np.asarray(resultado["y_pred_test"])

    minimo = min(y_real.min(), y_previsto.min())
    maximo = max(y_real.max(), y_previsto.max())

    plt.figure(figsize=(9, 7))
    sns.scatterplot(x=y_real, y=y_previsto, alpha=0.45, s=25)
    plt.plot(
        [minimo, maximo],
        [minimo, maximo],
        linestyle="--",
        linewidth=2,
        label="Previsão perfeita",
    )

    metricas = resultado["metricas"]["teste"]
    plt.title("Valores reais × valores previstos (conjunto de teste)")
    plt.xlabel("Consumo real (kWh)")
    plt.ylabel("Consumo previsto (kWh)")
    plt.legend(
        title=(
            f"R² = {metricas['R2']:.3f}\n"
            f"MAE = {metricas['MAE']:.1f} kWh\n"
            f"RMSE = {metricas['RMSE']:.1f} kWh"
        )
    )
    salvar_grafico("03_valores_reais_vs_previstos.png")


def grafico_residuos(resultado):
    """Mostra os erros de previsão em função dos valores previstos."""
    y_previsto = np.asarray(resultado["y_pred_test"])
    residuos = np.asarray(resultado["y_test"]) - y_previsto

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_previsto, y=residuos, alpha=0.45, s=25)
    plt.axhline(0, linestyle="--", linewidth=2)

    plt.title("Análise dos resíduos do modelo")
    plt.xlabel("Consumo previsto (kWh)")
    plt.ylabel("Resíduo: real − previsto (kWh)")
    salvar_grafico("04_residuos.png")


def grafico_coeficientes(resultado):
    """Coeficientes reais do modelo treinado, ordenados por valor."""
    coeficientes = resultado["coeficientes"].sort_values()

    cor_positivo, cor_negativo = "#2a9d8f", "#e76f51"
    cores = [cor_positivo if valor >= 0 else cor_negativo for valor in coeficientes]

    fig, ax = plt.subplots(figsize=(11, max(6, 0.45 * len(coeficientes) + 2)))
    ax.barh(coeficientes.index, coeficientes.values, color=cores,
            edgecolor="black", linewidth=0.4)
    ax.axvline(0, color="black", linewidth=1.2)

    # Valor numérico ao lado de cada barra.
    deslocamento = np.abs(coeficientes.values).max() * 0.01
    for posicao, valor in enumerate(coeficientes.values):
        ax.text(
            valor + (deslocamento if valor >= 0 else -deslocamento),
            posicao,
            f"{valor:+.4f}",
            va="center",
            ha="left" if valor >= 0 else "right",
            fontsize=8,
        )

    # Folga lateral para os rótulos não ficarem cortados.
    minimo = min(coeficientes.min(), 0)
    maximo = max(coeficientes.max(), 0)
    folga = (maximo - minimo) * 0.12
    ax.set_xlim(minimo - folga, maximo + folga)

    ax.set_title("Coeficientes da regressão linear múltipla (modelo treinado)")
    ax.set_xlabel("Valor do coeficiente (variação em kWh por unidade da variável)")
    ax.set_ylabel("Variável")
    ax.legend(
        handles=[
            plt.Rectangle((0, 0), 1, 1, color=cor_positivo, label="Coeficiente positivo"),
            plt.Rectangle((0, 0), 1, 1, color=cor_negativo, label="Coeficiente negativo"),
        ],
        loc="lower right",
    )
    ax.grid(axis="y", visible=False)
    salvar_grafico("05_coeficientes_modelo.png")


def imprimir_modelo(resultado):
    """Imprime intercepto, coeficientes e equação do modelo treinado."""
    print(f"\nIntercepto: {resultado['modelo'].intercept_:.4f}")
    print("\nCoeficientes:")
    print(resultado["coeficientes"].round(4).to_string())
    print("\nEquação do modelo:")
    print(resultado["equacao"])


def main():
    if not ARQUIVO_DADOS.exists():
        raise FileNotFoundError(
            f"Não encontrei o arquivo de dados: {ARQUIVO_DADOS}\n"
            "Verifique se dados_pre_processado.csv está dentro da pasta raiz/dados."
        )

    PASTA_GRAFICOS.mkdir(exist_ok=True)

    print("Lendo dados pré-processados...")
    df = pd.read_csv(ARQUIVO_DADOS)

    if ALVO not in df.columns:
        raise ValueError(f"O dataset precisa conter a coluna '{ALVO}'.")

    print(f"Dataset: {len(df)} registros e {len(df.columns)} colunas.")

    print("\n1/5 - Gerando matriz de correlação...")
    grafico_correlacao(df)

    print("\n2/5 - Gerando gráficos de dispersão...")
    graficos_dispersao(df)

    # Sem modelo salvo em arquivo, treina com a divisão e a semente do projeto.
    print("\nTreinando o modelo...")
    resultado = treinar_modelo(caminho=str(ARQUIVO_DADOS))
    imprimir_modelo(resultado)

    print("\n3/5 - Gerando gráfico de valores reais x previstos...")
    grafico_real_vs_previsto(resultado)

    print("\n4/5 - Gerando gráfico de resíduos...")
    grafico_residuos(resultado)

    print("\n5/5 - Gerando gráfico dos coeficientes...")
    grafico_coeficientes(resultado)

    print("\nTodos os gráficos foram gerados!")
    print(f"Pasta de saída: {PASTA_GRAFICOS.resolve()}")


if __name__ == "__main__":
    main()
