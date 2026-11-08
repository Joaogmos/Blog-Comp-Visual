# O que ficou da disciplina

*08/11/2026*

No primeiro post eu escrevi que voltaria aqui no fim do semestre pra ver o
quanto a minha ideia de Computação Visual tinha mudado. Então tá aqui.

Eu achava que a matéria ia ser sobre interface, front-end, edição de imagem e
talvez um pouco de 3D. Errei quase tudo. A única coisa que acertei em parte foi
achar que ia aparecer IA com imagem, e mesmo isso veio de outro jeito: em vez de
reconhecimento facial pronto, o que ficou pra mim foi descobrir que uma rede
convolucional faz a mesma conta de um filtro de borrar, só que aprende os
números do kernel sozinha.

O que mais mudou a minha cabeça foi a coisa mais simples do semestre: imagem é
uma matriz de números. Escrito assim parece óbvio, mas depois disso quase tudo
virou "o que eu faço com esses números". No negativo e no contraste eu mexia em
cada pixel sozinho. Nos filtros de suavização passei a olhar os vizinhos. Nas
transformações geométricas mudava a posição dos pixels, e no Fourier a imagem
virava frequência. Quando eu escrevia cada post não via essa sequência, só
reparei agora relendo tudo.

Relendo também deu pra ver que o blog mudou no meio. Os posts 3 e 4 têm código
em C, fórmula e teste em cima de uma imagem. Do 5 em diante ficaram mais
curtos, mais resumo do que eu pesquisei do que coisa que eu testei. Se fosse
fazer de novo, eu tentaria rodar pelo menos um exemplo em cada post, porque é
rodando que a gente vê o filtro errando.

Onde eu mais aprendi foram os projetos, porque ali não dava pra só ler. No
projeto 1, em C com SDL3, mexer em pixel na mão mostrou o trabalho que tem por
trás de uma função que no OpenCV é uma linha. No projeto 2, com o Luis Felipe,
fizemos um tutorial de segmentação por cor em HSV, e foi ali que entendi por
que separar cor em RGB é chato: a iluminação mexe nos três canais ao mesmo
tempo, e no HSV ela fica quase toda num canal só.

Usei IA durante o semestre, pra programar e pra me ajudar nos posts. No projeto
1 isso me custou nota, porque ficou na cara. O que pesou foi eu não ter revisado
com atenção o que estava entregando. Depois disso passei a ler e a cortar mais
antes de mandar qualquer coisa, e é por isso que esse último post eu quis
escrever do meu jeito, mesmo que fique meio cru.

Voltando ao post 1: eu tinha dito que a parte mais interessante seria ensinar a
máquina a interpretar a imagem. Continuo achando. A diferença é que agora eu sei
que antes de interpretar alguma coisa ela precisa limpar ruído, ajustar
contraste e separar o objeto do fundo, e boa parte da disciplina foi
justamente isso.

---

[Voltar à página inicial](index.html)
