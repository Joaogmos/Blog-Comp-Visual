# Transformações geométricas e interpolação

*11/10/2026*

Depois de mexer só nos valores dos pixels (negativo, contraste), fui pesquisar
o outro tipo de operação: mexer na posição deles. Girar, ampliar ou deslocar
uma imagem parece simples, mas tem um problema escondido, e a solução dele é
o assunto principal deste post.

## As transformações básicas

As três transformações mais comuns são a translação (deslocar), a escala
(ampliar ou reduzir) e a rotação. Todas podem ser escritas como uma
multiplicação de matrizes. A rotação de um ângulo θ em torno da origem, por
exemplo, é:

```
x' = x·cos θ − y·sin θ
y' = x·sin θ + y·cos θ
```

A translação não cabe numa matriz 2x2, então se usa **coordenadas
homogêneas**, que acrescentam uma terceira coordenada e passam a usar matrizes
3x3. A vantagem é que assim as três transformações viram o mesmo tipo de
operação, e dá para combinar várias multiplicando as matrizes.

## O problema dos buracos

O jeito intuitivo de aplicar a transformação é percorrer a imagem original e
mandar cada pixel para a nova posição (mapeamento direto). O problema é que
duas coisas dão errado: alguns pixels de saída não recebem nenhum pixel de
entrada (ficam buracos), e outros recebem mais de um.

A solução padrão é o mapeamento inverso: percorrer a imagem de saída e, para
cada pixel, calcular de onde ele viria na imagem original usando a
transformação inversa. Assim nenhum pixel de saída fica sem valor.

Só que a posição calculada quase nunca é um número inteiro. Ela cai entre
pixels, e é aí que entra a interpolação.

## Métodos de interpolação

- **Vizinho mais próximo:** arredonda a posição e copia o pixel mais perto.
  É o mais rápido, mas deixa bordas serrilhadas.
- **Bilinear:** faz uma média ponderada dos 4 pixels em volta, com peso maior
  para os mais próximos. O resultado é mais suave, mas a imagem perde um pouco
  de nitidez.
- **Bicúbica:** usa os 16 pixels vizinhos (uma região 4x4). Costuma dar o
  melhor resultado visual entre os três, e custa mais processamento.

No OpenCV esses métodos aparecem como `INTER_NEAREST`, `INTER_LINEAR` e
`INTER_CUBIC`.

## Um detalhe que achei interessante

Aplicar várias transformações seguidas, com uma interpolação a cada uma, vai
acumulando o borrão da média. Por isso é melhor multiplicar todas as matrizes
primeiro e reamostrar a imagem uma única vez. Esse é um dos motivos de usar
matrizes homogêneas.

## O que eu aprendi

Mudar a posição dos pixels não é só uma conta de geometria: como a grade é
discreta, sempre há a decisão de qual valor colocar quando a posição cai entre
pixels. A escolha do método é um equilíbrio entre velocidade e qualidade
visual.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 2, seção sobre transformações geométricas e
  interpolação.
- OpenCV. *Geometric Transformations of Images*. https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html

---

[Voltar à página inicial](index.html)
