"""Post 6: rotacao de imagem com mapeamento inverso, vizinho mais proximo vs bilinear."""
import cv2
import numpy as np

from util import montagem, pasta_saida, psnr

SAIDA = pasta_saida(6)
N = 200


def imagem_teste():
    img = np.full((N, N), 200, np.uint8)
    for i in range(0, N, 20):                       # grade de linhas finas
        img[i, :] = 60
        img[:, i] = 60
    cv2.circle(img, (100, 100), 55, 30, 2)
    cv2.putText(img, "Rot", (62, 112), cv2.FONT_HERSHEY_SIMPLEX, 1.4, 0, 2, cv2.LINE_AA)
    cv2.rectangle(img, (10, 10), (N - 11, N - 11), 0, 1)
    return img


def rotacionar(img, graus, metodo):
    """Mapeamento inverso: para cada pixel de saida, descubro de onde ele veio na entrada."""
    h, w = img.shape
    cy, cx = (h - 1) / 2, (w - 1) / 2
    t = np.deg2rad(graus)
    c, s = np.cos(t), np.sin(t)
    y, x = np.mgrid[0:h, 0:w].astype(np.float64)
    xs = c * (x - cx) + s * (y - cy) + cx           # rotacao inversa
    ys = -s * (x - cx) + c * (y - cy) + cy
    fora = (xs < 0) | (xs > w - 1) | (ys < 0) | (ys > h - 1)
    if metodo == "vizinho":
        v = img[np.clip(np.rint(ys).astype(int), 0, h - 1), np.clip(np.rint(xs).astype(int), 0, w - 1)].astype(np.float64)
    else:                                           # bilinear
        x0 = np.clip(np.floor(xs).astype(int), 0, w - 2)
        y0 = np.clip(np.floor(ys).astype(int), 0, h - 2)
        fx, fy = np.clip(xs - x0, 0, 1), np.clip(ys - y0, 0, 1)
        f = img.astype(np.float64)
        v = (f[y0, x0] * (1 - fx) * (1 - fy) + f[y0, x0 + 1] * fx * (1 - fy)
             + f[y0 + 1, x0] * (1 - fx) * fy + f[y0 + 1, x0 + 1] * fx * fy)
    v[fora] = 200                                   # cor do fundo
    return np.clip(np.rint(v), 0, 255).astype(np.uint8)


def main():
    img = imagem_teste()
    cv2.imwrite(str(SAIDA / "original.png"), img)

    # confere minha rotacao bilinear com o warpAffine do OpenCV (rotacao de 30 graus)
    m = cv2.getRotationMatrix2D(((N - 1) / 2, (N - 1) / 2), -30, 1.0)
    ref = cv2.warpAffine(img, m, (N, N), flags=cv2.INTER_LINEAR, borderValue=200)
    minha = rotacionar(img, 30, "bilinear")
    d = np.abs(minha.astype(int) - ref.astype(int))
    print(f"vs OpenCV: {(d > 3).sum()} de {d.size} pixels diferem mais de 3 niveis, PSNR {psnr(minha, ref):.1f} dB")

    # 1 rotacao de 30 graus
    viz, bil = rotacionar(img, 30, "vizinho"), rotacionar(img, 30, "bilinear")
    montagem([("original", img), ("30 graus, vizinho", viz), ("30 graus, bilinear", bil)], 3, SAIDA / "uma_rotacao.png")

    # ampliacao do mesmo recorte para ver o serrilhado
    rec = lambda a: cv2.resize(a[20:80, 20:80], None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
    montagem([("vizinho (zoom)", rec(viz)), ("bilinear (zoom)", rec(bil))], 2, SAIDA / "zoom.png")

    # 12 rotacoes de 30 graus = volta completa. Quanto sobra da imagem original?
    print("== 12 x 30 graus (volta completa) ==")
    resultados = []
    for metodo in ("vizinho", "bilinear"):
        a = img.copy()
        for _ in range(12):
            a = rotacionar(a, 30, metodo)
        # comparar so o miolo (os cantos ja foram cortados nas rotacoes)
        miolo = (slice(30, N - 30), slice(30, N - 30))
        print(f"{metodo}: PSNR do miolo vs original = {psnr(img[miolo], a[miolo]):.2f} dB")
        resultados.append((f"12x30 graus, {metodo}", a))
    # uma rotacao unica de 360 graus nao muda nada; o problema e acumular reamostragens
    montagem([("original", img)] + resultados, 3, SAIDA / "volta_completa.png")


if __name__ == "__main__":
    main()
