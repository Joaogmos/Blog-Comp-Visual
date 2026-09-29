# Filtros de suavização: média, gaussiano e mediana

*25/09/2026*

Nos posts 3 e 4 o novo valor de cada pixel dependia só do valor antigo dele.
Dessa vez pesquisei um tipo de filtro que olha também para os vizinhos: o
filtro de suavização, usado para diminuir ruído.

## Como funciona

O filtro usa uma janela pequena, o kernel (por exemplo 3x3), que passa por
cima da imagem. Para cada pixel, o resultado é calculado com os pixels que
estão dentro da janela. Mudando o cálculo, muda o efeito.

## Filtro da média

Cada pixel vira a média dos pixels da janela. Num kernel 3x3, são 9 pixels, cada
um com peso 1/9. O resultado é uma imagem mais borrada: o ruído diminui, mas os
detalhes e as bordas também ficam borrados. Quanto maior a janela, maior o
borrão.

## Filtro gaussiano

É parecido com o da média, mas os pixels perto do centro pesam mais do que os
mais distantes. Por isso o borrão costuma ficar mais natural. O quanto ele
borra é controlado por um parâmetro chamado sigma.

## Filtro da mediana

Aqui não tem média: os valores da janela são colocados em ordem e o pixel
recebe o valor do meio. Esse filtro funciona bem contra o ruído do tipo "sal e
pimenta" (pontos pretos e brancos espalhados), porque os valores extremos nunca
ficam no meio da lista e acabam descartados.

## O que eu aprendi

Suavizar sempre troca uma coisa por outra: tira ruído, mas tira também um pouco
de detalhe. Para ruído espalhado o gaussiano costuma ir bem, e para pontos
pretos e brancos isolados a mediana é melhor. O OpenCV tem uma função para cada
um: `cv2.blur`, `cv2.GaussianBlur` e `cv2.medianBlur`.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 3 (filtragem espacial).
- OpenCV. *Smoothing Images*. https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html

---

[Voltar à página inicial](index.html)
