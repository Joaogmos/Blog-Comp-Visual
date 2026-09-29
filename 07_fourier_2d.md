# A transformada de Fourier aplicada a imagens

*25/10/2026*

No post 2 eu falei de filtros que olham a vizinhança de cada pixel. Pesquisando
mais, descobri que dá para analisar uma imagem de outro jeito: pelas
frequências que ela tem. Isso é feito com a transformada de Fourier.

## A ideia

A transformada de Fourier mostra que uma imagem pode ser vista como uma soma de
ondas de frequências diferentes:

- frequências baixas são as partes lisas e as mudanças suaves, como o fundo;
- frequências altas são as mudanças rápidas, como bordas, detalhes e ruído.

O resultado da transformada é chamado de espectro. Normalmente ele é mostrado
com o centro representando as frequências baixas e as frequências crescendo em
direção às pontas.

## Para que serve

Com o espectro dá para filtrar a imagem:

- filtro passa-baixa: mantém só as frequências baixas, e a imagem fica
  borrada, sem ruído;
- filtro passa-alta: mantém só as frequências altas, e sobram as bordas e os
  detalhes.

Isso é parecido com o que o filtro de suavização do post 5 faz, só que visto
por outro lado. Outra aplicação que achei interessante é remover ruído em
forma de listras: no espectro elas aparecem como pontos brilhantes isolados, e
apagando esses pontos as listras somem da imagem.

## O que eu aprendi

A transformada de Fourier não muda a imagem, só muda a forma de olhar para ela.
Alguns problemas, como as listras repetidas, ficam bem mais fáceis de resolver
olhando o espectro do que olhando os pixels.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 4 (filtragem no domínio da frequência).
- NumPy. *Discrete Fourier Transform (numpy.fft)*. https://numpy.org/doc/stable/reference/routines.fft.html

---

[Voltar à página inicial](index.html)
