# Análise de Séries Temporais: Média Móvel e FAC (ACF)

Este projeto contém scripts em Python para demonstrar conceitos fundamentais de Séries Temporais, incluindo Média Móvel Simples (SMA), processos de Média Móvel ($MA$) e a Funções de Autocorrelação (FAC/ACF).

---

## Explicação dos Exercícios

### 1. Suavização por Média Móvel Simples (Exemplo 1)
* **O que faz:** Cria uma série temporal sintética com tendência contínua e ruído aleatório, aplicando Médias Móveis Simples (SMA) de 7 e 14 dias.
* **Resolução:** Utiliza a função `.rolling().mean()` do `pandas` para calcular as médias móveis e plota o resultado com `matplotlib` para mostrar como a janela maior (14 dias) suaviza mais a curva de vendas do que a janela menor (7 dias).

---

### 2. Simulação de Modelo Estocástico MA(2) (Exemplo 2)
* **O que faz:** Simula o comportamento de um processo estocástico de Média Móvel de ordem 2 ($MA(2)$), onde o valor atual depende dos erros do presente e dos últimos dois dias ($t-1$ e $t-2$).
* **Resolução:** Utiliza o objeto `ArmaProcess` da biblioteca `statsmodels` com os parâmetros $MA = [1, 0.6, -0.3]$ para gerar 500 amostras e salva um gráfico demonstrando a volatilidade desse processo.

---

### 3. Cálculo da FAC Amostral e Correlograma (Exemplo 3)
* **O que faz:** Gera um conjunto de dados aleatórios e calcula a Função de Autocorrelação (FAC/ACF) até o *lag* 10, além de exibir o gráfico do correlograma.
* **Resolução:** Executa a função `stattools.acf` para obter os valores de autocorrelação numérica e a função `plot_acf` com intervalo de confiança de 95% para visualizar se há dependência temporal na série.

---

### 4. Diagnóstico de FAC em Processo MA(1) (Exemplo 4)
* **O que faz:** Simula um processo $MA(1)$ para evidenciar a propriedade teórica de "corte abrupto" da FAC após o *lag* $q$ (neste caso, *lag* 1).
* **Resolução:** Utiliza `ArmaProcess` com coeficiente $MA = [1, -0.8]$ em 1000 amostras e plota o correlograma, mostrando visualmente que apenas o primeiro *lag* possui autocorrelação significativa antes de cortar para zero.

---

### 5. Comparativo entre FAC Teórica e FAC Amostral (Exemplo 5)
* **O que faz:** Compara diretamente os valores matemáticos exatos da FAC (teórica) contra os valores calculados a partir de uma amostra finita ($N=200$) de um processo $MA(1)$.
* **Resolução:** Calcula `processo.acf()` (teórica) e `stattools.acf()` (amostral), plotando ambas lado a lado com um gráfico de hastes (`plt.stem`) para demonstrar como a amostra real se aproxima da teoria.

---

### 6. Teste de Ruído Branco via Ljung-Box (Exemplo 6)
* **O que faz:** Aplica um teste estatístico para verificar se uma determinada série temporal é composta puramente por Ruído Branco (dados totalmente aleatórios e sem autocorrelação).
* **Resolução:** Utiliza a função `acorr_ljungbox` nos *lags* 5 e 10 sobre uma série normal, retornando o p-valor para confirmar a hipótese nula de ausência de autocorrelação.