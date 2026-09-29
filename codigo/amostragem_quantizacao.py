"""Post 5: o que se perde ao reduzir resolucao (amostragem) e niveis de cinza (quantizacao)."""
import cv2
import numpy as np

from util import montagem, pasta_saida, psnr

SAIDA = pasta_saida(5)
N = 256


def imagem_teste():
    y, x = np.mgrid[0:N, 0:N].astype(np.float64)
    # metade de cima: degrade suave; metade de baixo: padrao de frequencia crescente
    img = np.zeros((N, N))
    img[:N // 2] = 40 + 180 * (x[:N // 2] / N)
    freq = 0.002 + 0.14 * (x[N // 2:] / N)          # ciclos por pixel, cresce para a direita
    fase = 2 * np.pi * np.cumsum(freq, axis=1)
    img[N // 2:] = 128 + 100 * np.sin(fase)
    out = np.clip(img, 0, 255).astype(np.uint8)
    cv2.circle(out, (64, 64), 30, 250, -1)
    return out


def reduzir_pulando(img, k):
    return img[::k, ::k]


def reduzir_media(img, k):
    h, w = img.shape
    return img.reshape(h // k, k, w // k, k).mean(axis=(1, 3)).round().astype(np.uint8)


def ampliar(img, k):
    return np.kron(img, np.ones((k, k), dtype=np.uint8))


def quantizar(img, niveis):
    passo = 256 / niveis
    return (np.floor(img / passo) * passo + passo / 2).astype(np.uint8)


def main():
    img = imagem_teste()
    cv2.imwrite(str(SAIDA / "original.png"), img)

    print("== amostragem ==")
    quadros = [("original 256x256", img)]
    for k in (2, 4, 8):
        a = ampliar(reduzir_pulando(img, k), k)
        b = ampliar(reduzir_media(img, k), k)
        print(f"k={k}: pulando {psnr(img, a):.2f} dB | media antes {psnr(img, b):.2f} dB")
        quadros += [(f"pulando 1 a cada {k}", a), (f"media {k}x{k} antes", b)]
    montagem(quadros, 3, SAIDA / "amostragem.png")

    print("== quantizacao ==")
    quadros = [("256 niveis", img)]
    for n in (32, 8, 4, 2):
        q = quantizar(img, n)
        print(f"{n} niveis: {psnr(img, q):.2f} dB, valores distintos = {len(np.unique(q))}")
        quadros.append((f"{n} niveis", q))
    montagem(quadros, 3, SAIDA / "quantizacao.png")

    # so o degrade (metade de cima), esticado para ver os "degraus"
    topo = img[:N // 2 - 10, 100:]
    faixa = [(f"{n} niveis", cv2.resize(quantizar(topo, n), (topo.shape[1] * 3, 70), interpolation=cv2.INTER_NEAREST)) for n in (256, 16, 8, 4)]
    montagem(faixa, 1, SAIDA / "degraus.png")


if __name__ == "__main__":
    main()
