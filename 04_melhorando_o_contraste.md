# Melhorando o contraste da foto revelada

*15/09/2026*

No post anterior fiquei com uma pergunta em aberto: a foto que "revelei" a partir
de um negativo antigo ficou escura e sem contraste. O que dá para fazer para
melhorar? Este post é a tentativa de responder, testando três transformações de
intensidade em cima da mesma imagem.

Todas elas continuam sendo **ponto a ponto**: o novo valor de um pixel depende
só do valor antigo dele. A diferença para o negativo é que agora a função não é
uma simples inversão.

## 1. Alargamento de contraste (contrast stretching)

A ideia mais direta: se a imagem só usa a faixa de `[a, b]` em vez de `[0, 255]`,
basta remapear linearmente essa faixa para o intervalo cheio.

```
S = (E - a) * 255 / (b - a)
```

com `a` e `b` sendo, por exemplo, o menor e o maior valor presentes na imagem
(ou percentis, tipo 2% e 98%, para não deixar um único pixel espúrio dominar).

```c
Uint8 a = 40, b = 130; // medidos no histograma da imagem
for (int i = 0; i < total; i += 4) {
    for (int c = 0; c < 3; c++) {
        int v = pixels[i + c];
        v = (v - a) * 255 / (b - a);
        v = v < 0 ? 0 : (v > 255 ? 255 : v); // clamp
        pixels[i + c] = (Uint8)v;
    }
}
```

No caso da minha foto isso já resolveu boa parte do problema: os rostos e o
ônibus ficaram bem mais separados do fundo.

## 2. Correção gama

O alargamento é linear. Às vezes o problema não é a faixa, e sim a distribuição:
a imagem está escura demais (ou clara demais) no meio-tom. A correção gama
resolve isso com uma curva:

```
S = 255 * (E / 255) ^ gamma
```

- `gamma < 1` clareia os tons médios e escuros (foi o meu caso);
- `gamma > 1` escurece;
- `gamma = 1` não faz nada.

Como envolve `pow`, o jeito prático é pré-calcular uma **lookup table** de 256
posições uma vez e depois só indexar:

```c
Uint8 lut[256];
double gamma = 0.6;
for (int i = 0; i < 256; i++) {
    double s = 255.0 * pow(i / 255.0, gamma);
    lut[i] = (Uint8)(s + 0.5);
}
for (int i = 0; i < total; i += 4) {
    pixels[i + 0] = lut[pixels[i + 0]];
    pixels[i + 1] = lut[pixels[i + 1]];
    pixels[i + 2] = lut[pixels[i + 2]];
}
```

Esse truque da LUT vale para qualquer transformação ponto a ponto — inclusive o
negativo e o alargamento acima.

## 3. Equalização de histograma

As duas anteriores exigem eu olhar a imagem e escolher parâmetros (`a`, `b`,
`gamma`). A equalização de histograma é **automática**: ela usa a função de
distribuição acumulada (CDF) dos níveis de intensidade como função de
transformação, o que tende a espalhar os valores por toda a faixa e deixar o
histograma mais "plano".

Passos:

1. Contar quantos pixels têm cada intensidade (histograma `h[0..255]`).
2. Calcular a soma acumulada `cdf[i] = h[0] + ... + h[i]`.
3. Normalizar: `lut[i] = round(255 * (cdf[i] - cdf_min) / (N - cdf_min))`, com
   `N` = total de pixels.
4. Aplicar a `lut` na imagem.

```c
int hist[256] = {0};
int n = surface->w * surface->h;
for (int i = 0; i < total; i += 4) {
    // luminância aproximada para decidir o mapeamento
    int y = (pixels[i] + pixels[i+1] + pixels[i+2]) / 3;
    hist[y]++;
}
int cdf[256]; int acc = 0;
for (int i = 0; i < 256; i++) { acc += hist[i]; cdf[i] = acc; }
int cdf_min = 0;
for (int i = 0; i < 256; i++) if (cdf[i] != 0) { cdf_min = cdf[i]; break; }
Uint8 lut[256];
for (int i = 0; i < 256; i++)
    lut[i] = (Uint8)(255.0 * (cdf[i] - cdf_min) / (n - cdf_min) + 0.5);
```

Aplicar a equalização direto nos três canais RGB costuma bagunçar a cor. O certo
é converter para um espaço que separe luminância de cor (YCbCr, HSV…),
equalizar só o canal de luminância e converter de volta. Como a minha foto era
praticamente monocromática (negativo P&B), deu para relevar isso.

## O que funcionou melhor

Para essa imagem específica, a combinação que deu o resultado mais legível foi:
**alargamento de contraste + uma correção gama leve** (`gamma ≈ 0,7`). A
equalização de histograma trouxe *mais* detalhe, mas também amplificou o ruído
da foto do celular e o granulado do filme — ficou com uma cara "dura".

A lição geral: o negativo do post anterior é só o primeiro passo. O trabalho de
verdade de "revelar" uma foto está em ajustar a **distribuição** das
intensidades, e quase sempre isso é um compromisso entre revelar detalhe e não
levantar ruído junto.

## Referências

- Gonzalez & Woods, *Digital Image Processing* — *Histogram Processing* e *Power-Law (Gamma) Transformations*.
- Documentação do OpenCV: `cv2.equalizeHist`, `cv2.LUT` e `cv2.createCLAHE` (versão local da equalização, que evita boa parte do problema de ruído).

---

[Voltar à página inicial](index.html)
