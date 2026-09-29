"""Post 7: espectro de Fourier 2D, filtro passa-baixa e remocao de listras periodicas."""
import cv2
import numpy as np

from util import montagem, pasta_saida, psnr

SAIDA = pasta_saida(7)
N = 256


def imagem_teste():
    img = np.full((N, N), 90, np.uint8)
    cv2.circle(img, (90, 100), 50, 220, -1)
    cv2.rectangle(img, (150, 60), (230, 170), 30, -1)
    cv2.line(img, (20, 210), (236, 190), 255, 3)
    cv2.putText(img, "Fourier", (40, 245), cv2.FONT_HERSHEY_SIMPLEX, 1.0, 255, 2, cv2.LINE_AA)
    return img


def espectro(img):
    return np.fft.fftshift(np.fft.fft2(img.astype(np.float64)))


def para_imagem(F):
    return np.clip(np.real(np.fft.ifft2(np.fft.ifftshift(F))), 0, 255).astype(np.uint8)


def visualizar(F):
    m = np.log1p(np.abs(F))
    return (255 * m / m.max()).astype(np.uint8)


def distancia_ao_centro():
    y, x = np.mgrid[0:N, 0:N]
    return np.hypot(x - N // 2, y - N // 2)


def main():
    img = imagem_teste()
    F = espectro(img)
    cv2.imwrite(str(SAIDA / "original.png"), img)
    cv2.imwrite(str(SAIDA / "espectro.png"), visualizar(F))

    # a transformada inversa devolve a imagem?
    print(f"ida e volta sem filtro: diferenca maxima = {np.abs(para_imagem(F).astype(int) - img).max()}")

    # 1) passa-baixa ideal (corta tudo fora de um raio) vs gaussiana no dominio da frequencia
    d = distancia_ao_centro()
    quadros = [("original", img)]
    print("== passa-baixa ==")
    for r in (10, 30):
        ideal = para_imagem(F * (d <= r))
        gauss = para_imagem(F * np.exp(-(d ** 2) / (2 * r ** 2)))
        print(f"raio {r}: ideal {psnr(img, ideal):.2f} dB | gaussiana {psnr(img, gauss):.2f} dB")
        quadros += [(f"ideal r={r}", ideal), (f"gaussiana s={r}", gauss)]
    montagem(quadros, 3, SAIDA / "passa_baixa.png")

    # 2) listras periodicas: aparecem como dois pontos no espectro
    y, x = np.mgrid[0:N, 0:N]
    listras = np.clip(img + 35 * np.sin(2 * np.pi * (x * 0.09 + y * 0.03)), 0, 255).astype(np.uint8)
    Fl = espectro(listras)
    mag = np.abs(Fl)
    mag[N // 2 - 4:N // 2 + 5, N // 2 - 4:N // 2 + 5] = 0        # ignora o centro (DC e vizinhos)
    py, px = np.unravel_index(np.argmax(mag), mag.shape)
    print(f"pico mais forte fora do centro: (u,v) = ({px - N // 2}, {py - N // 2}); esperado ~ ({round(0.09 * N)}, {round(0.03 * N)})")

    # zera uma vizinhanca pequena em volta do pico e do simetrico dele
    Fc = Fl.copy()
    for (cy, cx) in ((py, px), (N - py, N - px)):
        Fc[cy - 2:cy + 3, cx - 2:cx + 3] = 0
    limpa = para_imagem(Fc)
    print(f"listras: PSNR {psnr(img, listras):.2f} dB -> depois de zerar os picos {psnr(img, limpa):.2f} dB")

    marcado = cv2.cvtColor(visualizar(Fl), cv2.COLOR_GRAY2BGR)
    for (cy, cx) in ((py, px), (N - py, N - px)):
        cv2.circle(marcado, (cx, cy), 8, (0, 0, 255), 1)
    montagem([("com listras", listras), ("espectro (picos marcados)", marcado), ("depois do filtro", limpa)], 3, SAIDA / "listras.png")

    # 3) o mesmo passa-baixa gaussiano feito por convolucao no espacial (confere com o do dominio da frequencia)
    s = 2.0                                        # sigma espacial equivalente = N / (2*pi*sigma_freq)
    sigma_f = N / (2 * np.pi * s)
    via_freq = para_imagem(F * np.exp(-(d ** 2) / (2 * sigma_f ** 2)))
    via_esp = cv2.GaussianBlur(img, (0, 0), s, borderType=cv2.BORDER_WRAP)
    print(f"gaussiana: via frequencia vs via convolucao: PSNR {psnr(via_freq, via_esp):.1f} dB, diferenca max {np.abs(via_freq.astype(int) - via_esp).max()}")


if __name__ == "__main__":
    main()
