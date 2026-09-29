# Filtros de suavização: média, gaussiano e mediana

*25/09/2026*

Os posts 3 e 4 foram sobre transformações ponto a ponto, em que o novo valor de
um pixel depende só do valor antigo dele. Dessa vez fui pesquisar o passo
seguinte: filtros que olham também para os vizinhos. O mais simples deles é o
de suavização, usado para reduzir ruído e borrar detalhes pequenos.

## Filtragem espacial

Um filtro espacial percorre a imagem com uma janela pequena, o kernel (ou
máscara), normalmente 3x3 ou 5x5. Em cada posição, o pixel de saída é calculado
a partir dos pixels que estão sob a janela. Quando esse cálculo é uma soma
ponderada, com um peso para cada posição do kernel, o filtro é linear e a
operação se chama convolução (ou correlação, dependendo de o kernel ser
espelhado ou não; para kernels simétricos dá no mesmo).

Mudando só os pesos do kernel, muda o efeito do filtro.

## Filtro da média

É o mais simples: todos os pesos são iguais e somam 1. Num kernel 3x3, cada
peso vale 1/9, e o pixel de saída é a média dos 9 pixels da janela. O efeito é
borrar: mudanças bruscas de intensidade são misturadas com a vizinhança, e por
isso o ruído diminui. O preço é que as bordas e os detalhes finos também ficam
borrados, e quanto maior o kernel, mais forte é o borrão.

## Filtro gaussiano

O filtro da média trata todos os vizinhos igual, inclusive os mais distantes.
O gaussiano dá mais peso ao centro e menos peso conforme a distância cresce,
seguindo a função gaussiana:

```
G(x, y) = 1 / (2πσ²) · e^(−(x² + y²) / (2σ²))
```

O parâmetro `σ` controla o quanto a imagem é suavizada. Na prática o kernel
é truncado numa janela de cerca de ±3σ, que já cobre quase todo o peso, e os
valores são normalizados para somar 1. Comparado com a média, o resultado
costuma ser um borrão mais natural, sem o aspecto de blocos.

Uma propriedade prática é que o kernel gaussiano é separável: em vez de uma
convolução 2D com um kernel `k x k`, dá para fazer duas convoluções 1D, uma
nas linhas e outra nas colunas. O custo por pixel cai de `k²` para `2k`
operações, o que faz diferença em kernels grandes.

## Filtro da mediana

A mediana não é uma soma ponderada: ela ordena os valores da janela e fica com
o do meio. Por isso é um filtro não linear, e não dá para representar como
um kernel de pesos. Ele é muito bom contra ruído do tipo "sal e pimenta", em
que alguns pixels ficam pretos ou brancos por engano. Esses valores extremos
nunca ficam no meio da lista ordenada, então são descartados em vez de
espalhados, como acontece na média. A mediana também preserva melhor as bordas
do que os filtros lineares.

## As bordas da imagem

Nas bordas da imagem, parte da janela cai fora dela. Existem algumas
estratégias para isso: preencher com zeros, replicar o pixel da borda, espelhar
a imagem ou simplesmente ignorar os pixels da borda. Cada uma dá um resultado
um pouco diferente perto das margens.

## Na prática

O OpenCV tem uma função para cada filtro: `cv2.blur` (média),
`cv2.GaussianBlur` e `cv2.medianBlur`, e a documentação explica como
cada uma funciona.

## O que eu aprendi

Suavizar sempre troca ruído por perda de detalhe: os filtros lineares reduzem
um e prejudicam o outro. A escolha do filtro depende do tipo de ruído. Para
ruído espalhado o gaussiano costuma ser uma boa escolha, e para pixels
isolados errados a mediana funciona melhor. O que mais me chamou atenção foi
ver que a mediana, mesmo sendo simples, foge da lógica de "kernel de pesos"
que eu tinha entendido até então.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 3, seção sobre filtragem espacial (filtros de
  suavização e filtros de estatística de ordem).
- OpenCV. *Smoothing Images*. https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html

---

[Voltar à página inicial](index.html)
