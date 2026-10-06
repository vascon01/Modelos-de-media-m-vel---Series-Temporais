import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_process import ArmaProcess  # * Modelo estocástico


# todo: Suavização por media movel simples
def exemplo_um():
    np.random.seed(42)
    datas = pd.date_range(
        start="2026-01-01", periods=100, freq="D"
    )  # ~Vai gerar 100 dias
    ruido = np.random.normal(
        0, 5, 100
    )  # ! media,desvio padrao,quantidade
    tendencia = np.linspace(
        10, 50, 100
    )  # * 10 é o inicio do valor e 50 é final
    vendas = tendencia + ruido

    df = pd.DataFrame({"Datas": datas, "Vendas": vendas}).set_index("Datas")
    df["Vendas"] = df["Vendas"].round(2)

    #! Media Movel Simples (SMA) de 7 a 14 dias

    df["SMA_7"] = df["Vendas"].rolling(window=7).mean()
    df["SMA_14"] = df["Vendas"].rolling(window=14).mean()
    print(df.tail(10))

    plt.figure(figsize=(8, 4))
    plt.plot(df.index, df["Vendas"], label="Vendas")
    plt.plot(df.index, df["SMA_7"], label="SMA de 7 dias")
    plt.plot(df.index, df["SMA_14"], label="SMA de 14 dias")
    plt.legend()
    plt.title("Exemplo 1 - Suavização por Média Móvel Simples")
    plt.show()


# todo: Simulação de modelo estocastico tem como peso os erros dos valores de dois dias atras
# Z_t = e_t + 0.6*e_{t-1} - 0.3*e_{t-2}
#! Estocastico palavra chique para probabilidade/imprevisto/acesso
#! É um modelo que calcula como os erros do passado pesao nos valores de hoje


def exemplo_dois():
    ar_params = np.array(
        [1]
    )  # ^ Seria um filtro na qual queremos somente o MA que seria a pesagem dos erros caso quisesemos os dois AR mede como os valores de hoje dependem dos anteriores
    ma_params = np.array(
        [1, 0.6, -0.3]
    )  # ? Ma(erro de hoje,erro de ontem,erro de anteontem)

    processo_ma2 = ArmaProcess(ar_params, ma_params)

    # Simulação de 500 obs
    np.random.seed(123)
    dados_ma2 = processo_ma2.generate_sample(
        nsample=500
    )  # !Sorteia os erros aleatorios usa a formula de MA(2) e retorna um array com 500 numeros na serie temporal
    plt.figure(figsize=(8, 3))
    plt.plot(dados_ma2, color="navy", linewidth=1)
    plt.title("Serie Temporal Simulada de um Processo MA(2)")
    plt.savefig("ma2_simulation.png")
    plt.show()


# todo: Exemplo 3 - Cálculo da FAC Amostral e Visualização do Correlograma
def exemplo_tres():
    np.random.seed(42)
    serie = np.random.randn(200)

    fac_valores = sm.tsa.stattools.acf(serie, nlags=10)
    print("Valores da FAC (lags 0 a 10):")
    print(np.round(fac_valores, 3))

    fig, ax = plt.subplots(figsize=(8, 3))
    plot_acf(serie, lags=20, ax=ax, alpha=0.05)
    plt.title("Correlograma (FAC Amostral)")
    plt.savefig("acf_plot.png")
    plt.show()


# todo: Exemplo 4 - Diagnóstico de FAC em Processo MA(1)
def exemplo_quatro():
    ar_ma1 = np.array([1])
    ma_ma1 = np.array([1, -0.8])

    processo_ma1 = ArmaProcess(ar_ma1, ma_ma1)
    dados_ma1 = processo_ma1.generate_sample(nsample=1000)

    fig, ax = plt.subplots(figsize=(8, 3))
    plot_acf(
        dados_ma1,
        lags=10,
        ax=ax,
        title="FAC do MA(1): Identificacao do Corte no Lag 1",
    )
    plt.show()


# todo: Exemplo 5 - Comparativo entre FAC Teórica e FAC Amostral
def exemplo_cinco():
    ar = np.array([1])
    ma = np.array([1, -0.7])

    processo = ArmaProcess(ar, ma)
    fac_teorica = processo.acf(lags=11)

    np.random.seed(42)
    dados_amostra = processo.generate_sample(nsample=200)
    fac_amostral = sm.tsa.stattools.acf(dados_amostra, nlags=10)

    lags = np.arange(11)

    plt.figure(figsize=(8, 4))
    plt.stem(
        lags,
        fac_teorica,
        linefmt="r-",
        markerfmt="ro",
        basefmt="k-",
        label="FAC Teórica",
    )
    plt.stem(
        lags + 0.15,
        fac_amostral,
        linefmt="b--",
        markerfmt="bo",
        basefmt="k-",
        label="FAC Amostral (N=200)",
    )
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Comparativo: FAC Teórica vs. FAC Amostral em Processo MA(1)")
    plt.xlabel("Lags (k)")
    plt.ylabel("Autocorrelação")
    plt.legend()
    plt.savefig("fac_teorica_vs_amostral.png")
    plt.show()


# todo: Exemplo 6 - Teste de Ruído Branco via Ljung-Box
def exemplo_seis():
    np.random.seed(42)
    dados_ruido = np.random.normal(0, 1, 300)

    resultado_lb = acorr_ljungbox(dados_ruido, lags=[5, 10], return_df=True)
    print("Resultado do Teste de Ljung-Box:")
    print(resultado_lb)


# --- INICIADOR INTERATIVO EM LOOP ---
def main():
    while True:
        print("\n==========================================")
        print("    ESCOLHA O EXEMPLO PARA EXECUTAR       ")
        print("==========================================")
        print("1. Exemplo 1 - Suavização por Média Móvel Simples")
        print("2. Exemplo 2 - Simulação de Modelo MA(2)")
        print("3. Exemplo 3 - FAC Amostral e Correlograma")
        print("4. Exemplo 4 - Diagnóstico de FAC em Processo MA(1)")
        print("5. Exemplo 5 - Comparativo FAC Teórica vs. Amostral")
        print("6. Exemplo 6 - Teste de Ljung-Box (Ruído Branco)")
        print("0. Sair")
        print("==========================================")

        opcao = input("Digite o número da opção desejada: ").strip()

        if opcao == "1":
            exemplo_um()
        elif opcao == "2":
            exemplo_dois()
        elif opcao == "3":
            exemplo_tres()
        elif opcao == "4":
            exemplo_quatro()
        elif opcao == "5":
            exemplo_cinco()
        elif opcao == "6":
            exemplo_seis()
        elif opcao == "0" or opcao.lower() == "sair":
            print("\nExecução encerrada com sucesso!")
            break
        else:
            print("\nOpção inválida! Escolha um número entre 0 e 6.")


if __name__ == "__main__":
    main()