# Limiarização e morfologia: separando objetos do fundo

*08/11/2026*

Um problema comum em visão computacional é separar os objetos do fundo da
imagem. Pesquisei duas ferramentas simples para isso: a limiarização e a
morfologia.

## Limiarização

Escolhe-se um valor, o limiar, e cada pixel é classificado: se for mais claro
que o limiar, vira branco (objeto); senão, vira preto (fundo). O resultado é uma
imagem só de preto e branco.

O difícil é escolher o limiar. Existe um método automático chamado método de
Otsu, que olha o histograma da imagem e escolhe o valor que separa melhor os
pixels claros dos escuros. Ele funciona bem quando a imagem tem objetos claros
sobre um fundo escuro (ou o contrário), mas costuma ir mal quando a iluminação
é muito irregular.

## Morfologia

Depois da limiarização sobram pontinhos de ruído e falhas nos objetos. A
morfologia trabalha na imagem preto e branco usando uma pequena forma que passa
por cima dela. As duas operações básicas são:

- erosão: encolhe os objetos e apaga os pontos pequenos;
- dilatação: engorda os objetos e fecha buracos pequenos.

Fazendo uma seguida da outra dá para limpar a imagem. Erosão e depois
dilatação, por exemplo, remove o ruído e mantém o tamanho dos objetos grandes.

## Contando objetos

Com a imagem limpa, dá para contar quantos objetos existem: cada grupo de
pixels brancos ligados entre si conta como um objeto. Se dois objetos estiverem
encostados, eles são contados como um só.

## O que eu aprendi

Um problema que parece difícil, como contar objetos numa imagem, pode ser
resolvido em passos simples: separar com um limiar, limpar com a morfologia e
contar os grupos de pixels.

## Referências

- OTSU, N. A threshold selection method from gray-level histograms. *IEEE
  Transactions on Systems, Man, and Cybernetics*, v. 9, n. 1, p. 62-66, 1979.
- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São
  Paulo: Pearson, 2010. Capítulo 9 (morfologia) e capítulo 10 (segmentação).
- OpenCV. *Image Thresholding*. https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html

---

[Voltar à página inicial](index.html)
