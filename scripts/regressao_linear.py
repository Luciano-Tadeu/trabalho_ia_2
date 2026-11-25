"""
Regressão Linear Múltipla - Previsão de consumo de energia elétrica residencial (kWh)

Uso:
    python regressao_linear.py

Para o colega dos gráficos, basta importar:
    from modelo_regressao import treinar_modelo
    r = treinar_modelo()
    # r["modelo"], r["X_train"], r["X_test"], r["y_train"], r["y_test"],
    # r["y_pred_train"], r["y_pred_test"], r["metricas"], r["coeficientes"]
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split

ARQUIVO = "../dados/dados_pre_processado.csv"
ALVO = "kwh"
TEST_SIZE = 0.2
SEED = 42


def calcular_metricas(y_real, y_pred, n_features):
    n = len(y_real)
    r2 = r2_score(y_real, y_pred)
    r2_aj = 1 - (1 - r2) * (n - 1) / (n - n_features - 1)
    mse = mean_squared_error(y_real, y_pred)
    return {
        "R2": r2,
        "R2_ajustado": r2_aj,
        "MAE": mean_absolute_error(y_real, y_pred),
        "MSE": mse,
        "RMSE": np.sqrt(mse),
    }


def montar_equacao(modelo, colunas):
    termos = " ".join(f"{c:+.4f}*{n}" for n, c in zip(colunas, modelo.coef_))
    return f"{ALVO} = {modelo.intercept_:.4f} {termos}"


def treinar_modelo(caminho=ARQUIVO):
    df = pd.read_csv(caminho)
    X = df.drop(columns=[ALVO])
    y = df[ALVO]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred_train = modelo.predict(X_train)
    y_pred_test = modelo.predict(X_test)
    k = X.shape[1]

    cv = cross_val_score(LinearRegression(), X, y, cv=5, scoring="r2")

    return {
        "modelo": modelo,
        "X_train": X_train, "X_test": X_test,
        "y_train": y_train, "y_test": y_test,
        "y_pred_train": y_pred_train, "y_pred_test": y_pred_test,
        "metricas": {
            "treino": calcular_metricas(y_train, y_pred_train, k),
            "teste": calcular_metricas(y_test, y_pred_test, k),
            "cv_r2_media": cv.mean(),
            "cv_r2_desvio": cv.std(),
        },
        "coeficientes": pd.Series(modelo.coef_, index=X.columns),
        "equacao": montar_equacao(modelo, X.columns),
    }


if __name__ == "__main__":
    r = treinar_modelo()
    m = r["metricas"]

    print("=" * 60)
    print("MÉTRICAS")
    print("=" * 60)
    print(f"{'':14}{'Treino':>14}{'Teste':>14}")
    for nome in ["R2", "R2_ajustado", "MAE", "MSE", "RMSE"]:
        print(f"{nome:14}{m['treino'][nome]:>14.4f}{m['teste'][nome]:>14.4f}")
    print(f"\nValidação cruzada (5 folds) R²: {m['cv_r2_media']:.4f} ± {m['cv_r2_desvio']:.4f}")

    print("\n" + "=" * 60)
    print("COEFICIENTES")
    print("=" * 60)
    print(f"Intercepto: {r['modelo'].intercept_:.4f}")
    print(r["coeficientes"].round(4).to_string())

    print("\n" + "=" * 60)
    print("EQUAÇÃO DA RETA (hiperplano)")
    print("=" * 60)
    print(r["equacao"])