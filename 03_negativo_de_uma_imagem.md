# Transformação de intensidade: o negativo de uma imagem

*01/09/2026*

Depois de entender que, para o computador, uma imagem é só uma matriz de
intensidades, a pergunta natural é: o que acontece se eu mexer nesses números
um por um? Essa é a família das **transformações de intensidade** (ou
transformações ponto a ponto): o novo valor de cada pixel depende *só* do valor
antigo daquele mesmo pixel, sem olhar para os vizinhos. É o oposto da
convolução do post anterior.

## O negativo

A transformação mais simples dessa família é o **negativo**. A conta é:

```
S = (L - 1) - E
```

- `S`: pixel de saída;
- `L - 1`: intensidade máxima possível. Para 1 byte por pixel, `L - 1 = 255`;
- `E`: pixel de entrada.

Ou seja: o preto vira branco, o branco vira preto, e todos os tons no meio são
espelhados. É exatamente a relação entre um filme fotográfico negativo e a foto
revelada. Na aula o professor comentou que, se você tiver um negativo antigo em
mãos, dá para fotografar o filme com o celular e aplicar essa transformação
para "revelar" a imagem.

## O trecho de código (C + SDL3)

O núcleo do exemplo da disciplina é basicamente um laço sobre todos os pixels:

```c
// surface: imagem de entrada/saída, 1 byte por canal (RGBA)
Uint8 *pixels = (Uint8 *)surface->pixels;
int total = surface->w * surface->h * 4; // 4 bytes por pixel (RGBA)

for (int i = 0; i < total; i += 4) {
    pixels[i + 0] = 255 - pixels[i + 0]; // R
    pixels[i + 1] = 255 - pixels[i + 1]; // G
    pixels[i + 2] = 255 - pixels[i + 2]; // B
    // pixels[i + 3] (alpha) não é alterado
}
```

Não tem nada de sofisticado: `255 - valor` é a expressão `(L - 1) - E` com
`L - 1 = 255`. O custo é linear no número de pixels, e cada pixel é tratado de
forma independente — dá para paralelizar sem dor de cabeça.

## O experimento

Achei os negativos de algumas fotos do meu primeiro ano de graduação e usei um
deles como entrada. Fotografei o filme com o celular (imagem de entrada) e rodei
o código acima.

O resultado *já dá* para entender: um pessoal da faculdade viajou de ônibus para
Florianópolis/SC em 2002, para o XXII Congresso da Sociedade Brasileira de
Computação. Mas a imagem revelada ficou **feia**: escura, "lavada", com pouco
contraste. Parte da culpa é da foto do negativo tirada no celular (iluminação
irregular, reflexo do plástico do filme), mas mesmo uma digitalização perfeita
do negativo não resolveria tudo.

## Por que ficou com baixo contraste

O negativo é uma transformação **linear**: ele inverte a ordem dos tons, mas não
"estica" a faixa de intensidades. Se a foto original do negativo usava só uma
janelinha estreita de valores (digamos, de 40 a 130 em vez de 0 a 255), a
imagem invertida continua usando uma janela estreita — só que espelhada. O
histograma fica concentrado, e histograma concentrado é a definição de baixo
contraste.

Fica então a pergunta para o próximo post: **o que dá para fazer para melhorar
o resultado?** A resposta passa por outras transformações de intensidade —
alargamento de contraste, correção gama e equalização de histograma — que é o
que vou testar em cima dessa mesma foto.

## Referências

- Gonzalez & Woods, *Digital Image Processing* — capítulo de *Intensity Transformations and Spatial Filtering*.
- Material online da disciplina (exemplo `invert_image` em C + SDL3).

---

[Voltar à página inicial](index.html)
