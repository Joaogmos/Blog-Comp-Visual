# A transformada de Fourier aplicada a imagens

*25/10/2026*

No post 2 eu comentei que os filtros olham para a vizinhança de cada pixel. Pesquisando
mais, descobri que existe outro jeito de olhar para o mesmo problema: em vez
de pensar nos pixels, pensar nas frequências que compõem a imagem. Esse jeito
usa a transformada de Fourier.

## A ideia

Joseph Fourier propôs, no começo do século XIX, que uma função pode ser escrita
como uma soma de senos e cossenos de frequências diferentes. Para imagens, a
leitura é a seguinte:

- frequências baixas são as variações lentas, como o fundo liso e as grandes
  regiões de mesma cor;
- frequências altas são as mudanças rápidas, como bordas, texturas e ruído.

A transformada discreta 2D de uma imagem `f(x, y)` de tamanho `M x N` é:

```
F(u, v) = Σ Σ f(x, y) · e^(−j2π(ux/M + vy/N))
```

O resultado `F(u, v)` diz quanto de cada frequência existe na imagem. Em
implementações reais se usa a FFT (transformada rápida de Fourier, de Cooley e
Tukey, 1965), que reduz o custo de O(N²) para O(N log N).

## Como ler o espectro

Depois de reorganizar o resultado para deixar a frequência zero no centro, o
espectro mostra:

- o ponto central, que é a média de brilho da imagem;
- as frequências crescendo do centro para as bordas;
- linhas em cruz quando a imagem tem bordas retas, porque uma borda reta
  concentra energia numa direção do espectro.

Como os valores variam muito, o espectro costuma ser exibido em escala
logarítmica, senão só o centro aparece.

## Filtrar no espectro

O teorema da convolução diz que convoluir uma imagem com um kernel equivale a
multiplicar os espectros. Ou seja, a convolução do post 2, com um kernel de
suavização, pode ser vista como uma máscara que atenua as frequências altas. Alguns filtros no
domínio da frequência:

- **Passa-baixa ideal:** zera tudo fora de um raio do centro. Tem o problema de
  gerar ondulações em volta das bordas (efeito de anel, ou *ringing*), porque
  o corte é abrupto.
- **Gaussiano:** atenua de forma gradual e não produz o anel.
- **Butterworth:** fica entre os dois, com uma ordem que controla o quão
  abrupto é o corte.
- **Passa-alta:** faz o inverso, deixando bordas e detalhes.

Outra aplicação que achei legal é a remoção de ruído periódico. Um padrão
repetido, como listras, aparece no espectro como pontos brilhantes isolados.
Dá para zerar só esses pontos (filtro *notch*) e a listra some sem afetar o
resto da imagem, coisa difícil de fazer direto nos pixels.

## O que eu aprendi

A transformada de Fourier não muda a imagem, só muda a forma de descrevê-la.
Alguns problemas que são complicados no espaço, como ruído periódico, ficam
simples no espectro. E entendi que filtrar por kernel e filtrar no espectro
são o mesmo processo visto de dois lados.

## Referências

- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 4 (filtragem no domínio da frequência).
- COOLEY, J. W.; TUKEY, J. W. An algorithm for the machine calculation of
  complex Fourier series. *Mathematics of Computation*, v. 19, n. 90,
  p. 297-301, 1965.
- NumPy. *Discrete Fourier Transform (numpy.fft)*. https://numpy.org/doc/stable/reference/routines.fft.html

---

[Voltar à página inicial](index.html)
