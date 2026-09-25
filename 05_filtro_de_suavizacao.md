# Saindo do ponto a ponto: um filtro de suavização

*25/09/2026*

Os últimos posts foram todos sobre **transformações ponto a ponto**: o negativo
e as três formas de melhorar contraste. Em todas elas, o valor de saída de um
pixel dependia só do valor de entrada daquele mesmo pixel. Lá no post 2 eu já
tinha citado o conceito de **convolução** — filtro que olha para a vizinhança
de cada pixel —, mas nunca tinha implementado um. Este post é a primeira vez
que saio do ponto a ponto e mexo em filtro espacial de verdade.

## A ideia do filtro da média

O filtro mais simples dessa família é o de **suavização por média** (*mean
blur*): cada pixel de saída vira a média dos pixels numa janela ao redor dele
na imagem de entrada. Com uma janela 3x3, por exemplo:

```
S(x, y) = média de E(x+i, y+j), para i, j em [-1, 0, 1]
```

Isso é uma convolução com um kernel 3x3 onde todo peso vale `1/9`. O efeito é
borrar a imagem: variações bruscas de intensidade (ruído, bordas finas) ficam
misturadas com a vizinhança, então elas se atenuam.

## O trecho de código (C + SDL3)

Diferente do negativo, aqui não dá para escrever direto em cima da mesma
surface: o pixel `(x, y)` de saída depende de pixels vizinhos que ainda não
foram alterados, então preciso de um buffer de saída separado.

```c
// src: imagem de entrada; dst: buffer de saída, mesmo tamanho
Uint8 *src = (Uint8 *)in_surface->pixels;
Uint8 *dst = (Uint8 *)out_surface->pixels;
int w = in_surface->w, h = in_surface->h;

for (int y = 1; y < h - 1; y++) {
    for (int x = 1; x < w - 1; x++) {
        for (int c = 0; c < 3; c++) { // R, G, B
            int soma = 0;
            for (int j = -1; j <= 1; j++) {
                for (int i = -1; i <= 1; i++) {
                    int idx = ((y + j) * w + (x + i)) * 4 + c;
                    soma += src[idx];
                }
            }
            dst[(y * w + x) * 4 + c] = (Uint8)(soma / 9);
        }
    }
}
```

As bordas da imagem (`x` ou `y` no limite) ficaram de fora de propósito — dar
tratamento a elas (replicar borda, espelhar, ignorar) é um detalhe a mais que
deixei para uma próxima iteração.

## O experimento

Apliquei o filtro na mesma foto do negativo dos posts anteriores, já com o
alargamento de contraste feito. O granulado do filme (ruído de alta frequência)
diminuiu visivelmente, mas os contornos dos rostos e do ônibus também ficaram
mais moles — o preço de tratar ruído e borda da mesma forma.

Também testei aumentar a janela para 5x5: o efeito de borrão ficou bem mais
forte, o que confirma que o **tamanho do kernel** é o principal parâmetro de
quão agressiva é a suavização.

## Média vs. Gaussiana

O professor comentou em aula que o filtro da média tem um problema: todo pixel
da vizinhança pesa igual, incluindo os mais distantes do centro. O filtro
**Gaussiano** resolve isso dando mais peso ao centro e menos peso conforme a
distância aumenta (kernel gerado a partir da função gaussiana 2D), o que
costuma borrar de forma mais "natural" e com menos artefato de bloco. Fica
registrado como próximo filtro a implementar.

## Referências

- Gonzalez & Woods, *Digital Image Processing* — capítulo de *Spatial
  Filtering* (filtros lineares de suavização).
- Documentação do OpenCV: `cv2.blur` e `cv2.GaussianBlur`.

---

[Voltar à página inicial](index.html)
