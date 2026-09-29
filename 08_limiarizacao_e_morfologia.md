# Limiarização de Otsu e morfologia matemática

*08/11/2026*

Um problema comum em visão computacional é separar os objetos do fundo. Fui
pesquisar as ferramentas mais básicas para isso: a limiarização, que decide
quais pixels pertencem ao objeto, e a morfologia, que limpa o resultado.

## Limiarização

A ideia é escolher um valor `T` e classificar cada pixel: se a intensidade é
maior que `T`, é objeto; senão, é fundo. O resultado é uma imagem binária. O
difícil é escolher `T`, e olhar o histograma ajuda: quando há objetos claros
sobre um fundo escuro, o histograma tem dois picos, e um bom limiar fica no
vale entre eles.

## O método de Otsu

Nobuyuki Otsu propôs em 1979 um jeito automático de achar esse vale. Para cada
`T` possível, os pixels se dividem em duas classes, e o método escolhe o `T`
que maximiza a variância entre as classes:

```
σ²_B(T) = ω0(T) · ω1(T) · [μ0(T) − μ1(T)]²
```

Nessa fórmula, `ω0` e `ω1` são as proporções de pixels de cada classe e `μ0`
e `μ1` são as médias de intensidade delas. Na prática é escolher o limiar que
deixa as duas classes o mais separadas possível, e só precisa do histograma.

O método tem limitações. Funciona melhor quando o histograma é bimodal, e
tende a falhar quando a iluminação é irregular, porque um limiar único não
serve para a imagem inteira. Nesses casos se usa limiarização adaptativa, com
um limiar calculado por região.

## Morfologia matemática

Depois da limiarização costumam sobrar pequenos pontos de ruído e falhas nos
objetos. A morfologia trata a imagem binária com um elemento estruturante, uma
pequena forma (por exemplo um quadrado 3x3) que percorre a imagem. As
operações principais são:

- **Erosão:** um pixel só continua branco se todo o elemento estruturante
  couber dentro do objeto. Encolhe os objetos e apaga regiões pequenas.
- **Dilatação:** o contrário, um pixel fica branco se o elemento tocar o
  objeto em algum ponto. Engorda os objetos e fecha buracos pequenos.
- **Abertura:** erosão seguida de dilatação. Remove ruídos pequenos e
  mantém o tamanho dos objetos maiores.
- **Fechamento:** dilatação seguida de erosão. Fecha buracos e falhas.

A morfologia matemática foi desenvolvida na década de 1960 por Georges
Matheron e Jean Serra, na França, para estudar estruturas de minerais.

## Contar objetos

Com a imagem limpa dá para rotular os componentes conexos: cada grupo de
pixels brancos ligados entre si recebe um rótulo, e o número de rótulos
é a quantidade de objetos. Aqui importa o tipo de vizinhança, 4 (só lados) ou
8 (lados e diagonais), porque isso muda o que é considerado "ligado". Objetos
que se encostam viram um só componente, e separá-los exige outras técnicas,
como a transformada de distância com watershed.

## O que eu aprendi

Achei interessante que um problema que parece difícil, contar objetos numa
imagem, pode ser dividido em passos simples: escolher um limiar, limpar e
rotular. Também ficou claro que cada passo tem seu ponto fraco, como a
iluminação irregular para o Otsu e os objetos encostados para a contagem.

## Referências

- OTSU, N. A threshold selection method from gray-level histograms. *IEEE
  Transactions on Systems, Man, and Cybernetics*, v. 9, n. 1, p. 62-66, 1979.
- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 9 (morfologia) e capítulo 10 (segmentação).
- OpenCV. *Image Thresholding*. https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html

---

[Voltar à página inicial](index.html)
