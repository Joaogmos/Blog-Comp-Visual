"""Post 8: contar objetos em uma imagem (Otsu na mao, morfologia e componentes conexos)."""
from collections import deque

import cv2
import numpy as np

from util import montagem, pasta_saida

SAIDA = pasta_saida(8)
N = 320


def cena(rng, n_objetos=14, sigma=12):
    """Discos claros de tamanhos variados sobre fundo com iluminacao irregular e ruido."""
    y, x = np.mgrid[0:N, 0:N]
    fundo = 65 + 35 * (x / N) + 10 * np.sin(y / 40)            # brilho varia pela imagem
    img = fundo.copy()
    centros = []
    while len(centros) < n_objetos:
        cx, cy, r = rng.integers(25, N - 25), rng.integers(25, N - 25), rng.integers(9, 20)
        if all(np.hypot(cx - a, cy - b) > r + r2 + 6 for a, b, r2 in centros):    # sem encostar
            centros.append((cx, cy, r))
            img[np.hypot(x - cx, y - cy) <= r] = 175 + rng.integers(-15, 15)
    img += rng.normal(0, sigma, img.shape)
    # alguns pontinhos de sujeira que nao sao objetos
    for _ in range(25):
        px, py = rng.integers(0, N - 2), rng.integers(0, N - 2)
        img[py:py + 2, px:px + 2] = 230
    return np.clip(img, 0, 255).astype(np.uint8), len(centros)


def otsu(img):
    """Escolhe o limiar que maximiza a variancia entre as duas classes."""
    hist = np.bincount(img.ravel(), minlength=256).astype(np.float64)
    p = hist / hist.sum()
    w0 = np.cumsum(p)
    mu = np.cumsum(p * np.arange(256))
    mu_t = mu[-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        var_entre = (mu_t * w0 - mu) ** 2 / (w0 * (1 - w0))
    return int(np.nanargmax(var_entre))


def erodir(b, k=1):
    p = np.pad(b, k, constant_values=False)
    out = np.ones_like(b)
    for dy in range(2 * k + 1):
        for dx in range(2 * k + 1):
            out &= p[dy:dy + b.shape[0], dx:dx + b.shape[1]]
    return out


def dilatar(b, k=1):
    p = np.pad(b, k, constant_values=False)
    out = np.zeros_like(b)
    for dy in range(2 * k + 1):
        for dx in range(2 * k + 1):
            out |= p[dy:dy + b.shape[0], dx:dx + b.shape[1]]
    return out


def abertura(b, k=1):
    return dilatar(erodir(b, k), k)


def rotular(b):
    """Componentes conexos (vizinhanca de 4) por busca em largura. Devolve mapa de rotulos e areas."""
    h, w = b.shape
    rot = np.zeros((h, w), np.int32)
    areas = []
    for y in range(h):
        for x in range(w):
            if b[y, x] and rot[y, x] == 0:
                areas.append(0)
                idx = len(areas)
                rot[y, x] = idx
                fila = deque([(y, x)])
                while fila:
                    cy, cx = fila.popleft()
                    areas[-1] += 1
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < h and 0 <= nx < w and b[ny, nx] and rot[ny, nx] == 0:
                            rot[ny, nx] = idx
                            fila.append((ny, nx))
    return rot, areas


def pintar(rot):
    cores = np.random.default_rng(1).integers(60, 255, (rot.max() + 1, 3)).astype(np.uint8)
    cores[0] = 255
    return cores[rot]


def main():
    resultados = []
    for semente in range(5):
        rng = np.random.default_rng(semente)
        img, real = cena(rng)
        t = otsu(img)
        t_cv, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        bin_ = img > t
        _, areas_sem = rotular(bin_)
        limpa = abertura(bin_, 1)
        _, areas_ab = rotular(limpa)
        suave = cv2.medianBlur(img, 5)                     # mediana 5x5 antes do limiar
        t2 = otsu(suave)
        bin2 = suave > t2
        rot, areas = rotular(abertura(bin2, 1))
        print(f"cena {semente}: reais={real} | otsu={t} (OpenCV {t_cv:.0f}) | so limiar={len(areas_sem)} | limiar+abertura={len(areas_ab)} | mediana+limiar+abertura={len(areas)}")
        resultados.append((real, len(areas_sem), len(areas_ab), len(areas)))
        if semente == 0:
            cv2.imwrite(str(SAIDA / "cena.png"), img)
            hist = cv2.calcHist([img], [0], None, [256], [0, 256]).ravel()
            grafico = np.full((160, 256, 3), 255, np.uint8)
            for i, v in enumerate(hist):
                cv2.line(grafico, (i, 159), (i, 159 - int(150 * v / hist.max())), (90, 90, 90), 1)
            cv2.line(grafico, (t, 0), (t, 159), (0, 0, 255), 1)
            cv2.imwrite(str(SAIDA / "histograma.png"), cv2.resize(grafico, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST))
            montagem([("cena", img), ("so Otsu", bin_.astype(np.uint8) * 255),
                      ("Otsu + abertura", limpa.astype(np.uint8) * 255),
                      ("mediana+Otsu+abertura", abertura(bin2, 1).astype(np.uint8) * 255),
                      ("objetos rotulados", pintar(rot))],
                     2, SAIDA / "etapas.png", 0.9)
    for i, nome in enumerate(("so limiar", "limiar + abertura", "mediana + limiar + abertura"), start=1):
        print(f"erro total de contagem nas 5 cenas, {nome}: {sum(abs(r[0] - r[i]) for r in resultados)}")


def contar(img, mediana):
    base = cv2.medianBlur(img, 5) if mediana else img
    b = base > otsu(base)
    return len(rotular(abertura(b, 1))[1])


def varredura_de_ruido():
    """Mesmas 20 cenas com ruido cada vez maior: quantas vezes acerta a contagem?"""
    print("== variando o ruido (20 cenas por linha, 14 objetos cada) ==")
    for sigma in (12, 25, 35, 45):
        acertos = {False: 0, True: 0}
        erro = {False: 0, True: 0}
        for semente in range(20):
            img, real = cena(np.random.default_rng(100 + semente), sigma=sigma)
            for med in (False, True):
                c = contar(img, med)
                acertos[med] += c == real
                erro[med] += abs(c - real)
        print(f"sigma={sigma}: sem mediana acertou {acertos[False]}/20 (erro total {erro[False]}) | com mediana acertou {acertos[True]}/20 (erro total {erro[True]})")


if __name__ == "__main__":
    main()
    varredura_de_ruido()
