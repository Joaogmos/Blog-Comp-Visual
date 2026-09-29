"""Funcoes de apoio usadas pelos scripts dos posts (metricas e montagem de figuras)."""
from pathlib import Path

import cv2
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent


def pasta_saida(n):
    p = RAIZ / "img" / f"{n:02d}"
    p.mkdir(parents=True, exist_ok=True)
    return p


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def rotulo(img, texto):
    """Converte para BGR e escreve um rotulo no canto superior esquerdo."""
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        img = img.copy()
    cv2.rectangle(img, (0, 0), (8 + 9 * len(texto), 20), (255, 255, 255), -1)
    cv2.putText(img, texto, (4, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 0, 0), 1, cv2.LINE_AA)
    return img


def montagem(imagens, colunas, caminho, escala=1.0):
    """imagens: lista de (texto, array). Todas devem ter o mesmo tamanho."""
    quadros = [rotulo(im, t) for t, im in imagens]
    while len(quadros) % colunas:
        quadros.append(np.full_like(quadros[0], 255))
    linhas = [np.hstack(quadros[i:i + colunas]) for i in range(0, len(quadros), colunas)]
    grade = np.vstack(linhas)
    if escala != 1.0:
        grade = cv2.resize(grade, None, fx=escala, fy=escala, interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(caminho), grade)
