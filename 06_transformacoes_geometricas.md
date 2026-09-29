# Transformações geométricas e interpolação

*11/10/2026*

Até aqui eu só tinha visto operações que mudam o valor dos pixels. Dessa vez
pesquisei as que mudam a posição deles: mover, ampliar e girar uma imagem.

## As transformações

As mais básicas são a translação (mover a imagem), a escala (ampliar ou
reduzir) e a rotação (girar). Todas podem ser escritas com contas de
coordenadas: cada pixel tem uma posição (x, y), e a transformação calcula a
nova posição dele.

## O problema

Quando a imagem é girada ou ampliada, a nova posição de um pixel quase nunca cai
exatamente em cima de um pixel da grade. Se eu só mandasse cada pixel para a
posição nova, ficariam buracos na imagem final.

Por isso se faz o contrário: para cada pixel da imagem de saída, calcula-se de
onde ele veio na imagem original. Mas esse ponto de origem também costuma
cair entre pixels, e aí é preciso escolher um valor. Essa escolha se chama
interpolação.

## Tipos de interpolação

- Vizinho mais próximo: pega o valor do pixel mais perto. É rápido, mas deixa
  as bordas serrilhadas.
- Bilinear: faz uma média dos 4 pixels em volta, dando mais peso aos mais
  próximos. Fica mais suave.
- Bicúbica: usa 16 pixels em volta e costuma dar o melhor resultado, mas demora
  mais.

No OpenCV esses métodos aparecem como `INTER_NEAREST`, `INTER_LINEAR` e
`INTER_CUBIC`.

## O que eu aprendi

Mexer na posição dos pixels não é só geometria, porque a imagem é uma grade e
sempre é preciso decidir que valor colocar entre os pixels. A escolha do método
é um equilíbrio entre velocidade e qualidade.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 2 (interpolação e transformações geométricas).
- OpenCV. *Geometric Transformations of Images*. https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html

---

[Voltar à página inicial](index.html)
