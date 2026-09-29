# Amostragem e quantização: como uma cena vira imagem digital

*29/09/2026*

Nos posts anteriores eu tratei a imagem como uma matriz de números já pronta.
Dessa vez fui pesquisar de onde essa matriz vem. A resposta está em duas
etapas da digitalização, a amostragem e a quantização, e cada uma joga fora um
tipo de informação.

## Amostragem

Amostrar é escolher em quais pontos da cena eu vou medir a luz. Uma cena real é
contínua, e o sensor da câmera só consegue medir um número finito de posições,
organizadas numa grade. A quantidade de pontos dessa grade é a resolução
espacial da imagem: quanto menos pontos, menos detalhe fino cabe nela.

O ponto que mais me chamou atenção foi o aliasing. Pelo teorema de
Nyquist-Shannon, para representar bem um detalhe que se repete, como uma
listra, é preciso amostrar com pelo menos o dobro da frequência desse detalhe.
Se a grade for grossa demais, o detalhe não some: ele aparece como um padrão
falso, mais largo, que não existe na cena. O moiré que aparece ao fotografar
uma tela ou um tecido listrado é esse efeito.

Isso também vale ao reduzir uma imagem que já existe. Descartar pixels sem
cuidado gera aliasing, e por isso o comum é aplicar antes um filtro que
suavize a imagem (passa-baixa) e só depois diminuir. A documentação do OpenCV,
por exemplo, recomenda a interpolação `INTER_AREA` para reduzir imagens, que
faz justamente uma média sobre a área de origem de cada pixel.

## Quantização

Quantizar é decidir quantos valores diferentes um pixel pode ter. Com `k` bits
por pixel existem `L = 2^k` níveis de cinza. O padrão é 8 bits, ou 256 níveis
(de 0 a 255). O armazenamento cresce com os dois fatores: uma imagem de `M x N`
pixels com `k` bits ocupa `M · N · k` bits. Uma imagem de 1024x1024 com 8 bits,
por exemplo, tem 1 MiB.

Reduzir os níveis tem um efeito visível em regiões de transição suave, como um
céu ou uma parede com sombra. Em vez de um degradê contínuo aparecem faixas
com bordas nítidas, chamadas de falsos contornos. Os livros de processamento de
imagens costumam mostrar a mesma foto com 256, 128, 64 e assim por diante até 2
níveis para deixar isso claro.

## Resolução e níveis são coisas separadas

Uma imagem pode ter muitos pixels e poucos níveis, ou o contrário. Um
detalhe fino se perde quando falta resolução espacial, e um degradê fica
quebrado quando faltam níveis. Com isso entendi por que uma foto com poucos
pixels parece "quadriculada" e uma com poucos níveis parece "pintada em faixas".

## O que eu aprendi

Toda imagem digital já é uma aproximação, feita em duas direções: no espaço
(amostragem) e na intensidade (quantização). Os problemas que eu via sem saber
o nome, como o quadriculado e as faixas, são consequências diretas dessas duas
escolhas. Fiquei com vontade de ver mais sobre o filtro antes de reduzir, que
me pareceu a parte mais prática de tudo isso.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 2, seção sobre amostragem e quantização.
- OpenCV. *Geometric Image Transformations* (`cv::resize` e as opções de
  interpolação). https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html

---

[Voltar à página inicial](index.html)
