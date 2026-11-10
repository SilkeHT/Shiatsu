"""Retrato a línea roja: rasgos y pelo trazados de una foto, silueta dibujada a mano.
Uso: python retrato.py foto.jpg salida.svg x 50 130 40 42 115 18  (requiere opencv-python-headless)
La foto no se guarda en el repositorio; las coordenadas de la silueta son de la foto original."""
import sys
import cv2
import numpy as np

src, out_svg, out_png = sys.argv[1:4]
hair_lo, hair_hi, hair_min, face_lo, face_hi, face_min = (float(a) for a in sys.argv[4:10])

ROJO = "#B4485A"
img = cv2.imread(src)
X0, Y0, X1, Y1 = 180, 190, 1240, 1400
W, H = X1 - X0, Y1 - Y0

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)

def canny(bil, k, a, b):
    sm = cv2.bilateralFilter(gray, bil, 70, 70)
    sm = cv2.GaussianBlur(sm, (k, k), 0)
    return cv2.Canny(sm, a, b)

# Zonas
pelo = np.zeros(gray.shape, np.uint8)
cv2.fillPoly(pelo, [np.array([(300, 330), (420, 245), (640, 210), (860, 255), (1005, 420), (1020, 610),
                              (950, 790), (880, 840), (860, 700), (800, 560), (640, 520), (480, 560),
                              (440, 700), (430, 800), (330, 790), (285, 560)], np.int32)], 255)
pelo = cv2.erode(pelo, np.ones((13, 13), np.uint8))
cara = np.zeros(gray.shape, np.uint8)
cv2.ellipse(cara, (648, 775), (175, 225), 0, 0, 360, 255, -1)
cara[985:, :] = 0
cara[:618, :] = 0
cv2.ellipse(cara, (648, 650), (48, 52), 0, 0, 360, 0, -1)  # entrecejo
pelo[cara > 0] = 0

def trazos(edges, min_len, eps):
    edges = edges[Y0:Y1, X0:X1]
    cs, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        half = c[: len(c) // 2 + 1]
        if cv2.arcLength(half, False) < min_len:
            continue
        pts = cv2.approxPolyDP(half, eps, False)[:, 0, :].astype(float)
        if len(pts) < 2:
            continue
        d = f"M{pts[0][0]:.0f},{pts[0][1]:.0f}"
        for i in range(1, len(pts) - 1):
            mx, my = (pts[i] + pts[i + 1]) / 2
            d += f" Q{pts[i][0]:.0f},{pts[i][1]:.0f} {mx:.0f},{my:.0f}"
        d += f" L{pts[-1][0]:.0f},{pts[-1][1]:.0f}"
        out.append(d)
    return out

e_pelo = canny(9, 7, hair_lo, hair_hi); e_pelo[pelo == 0] = 0
e_cara = canny(9, 5, face_lo, face_hi); e_cara[cara == 0] = 0
p_pelo = trazos(e_pelo, hair_min, 2.0)
p_cara = trazos(e_cara, face_min, 1.4)

def m(x, y):  # foto -> lienzo
    return f"{x - X0},{y - Y0}"

a_mano = [
    # contorno de la cara (lado izquierdo y mentón hasta el lado derecho)
    f"M{m(452, 650)} C{m(442, 740)} {m(450, 830)} {m(478, 890)} C{m(510, 950)} {m(575, 1000)} {m(640, 1004)}"
    f" C{m(712, 1002)} {m(780, 955)} {m(818, 895)} C{m(846, 850)} {m(856, 760)} {m(852, 690)}",
    # cuello
    f"M{m(488, 935)} C{m(492, 990)} {m(478, 1040)} {m(452, 1078)}",
    f"M{m(812, 915)} C{m(808, 980)} {m(822, 1040)} {m(866, 1078)}",
    # escote barco
    f"M{m(415, 1088)} C{m(520, 1150)} {m(780, 1160)} {m(905, 1082)}",
    # hombros y brazos
    f"M{m(415, 1088)} C{m(330, 1110)} {m(250, 1140)} {m(215, 1200)} C{m(190, 1260)} {m(185, 1330)} {m(182, 1400)}",
    f"M{m(905, 1082)} C{m(1000, 1100)} {m(1090, 1140)} {m(1130, 1210)} C{m(1155, 1270)} {m(1165, 1340)} {m(1168, 1400)}",
    # pliegue de la manga
    f"M{m(300, 1250)} C{m(310, 1310)} {m(320, 1360)} {m(318, 1400)}",
]
botones = f'<circle cx="{868 - X0}" cy="{1132 - Y0}" r="7"/><circle cx="{892 - X0}" cy="{1124 - Y0}" r="4"/>'

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
       f'<g fill="none" stroke="{ROJO}" stroke-linecap="round" stroke-linejoin="round">'
       f'<g stroke-width="9">' + "".join(f'<path d="{p}"/>' for p in a_mano) + botones + "</g>"
       f'<g stroke-width="6.5">' + "".join(f'<path d="{p}"/>' for p in p_pelo) + "</g>"
       f'<g stroke-width="7">' + "".join(f'<path d="{p}"/>' for p in p_cara) + "</g>"
       "</g></svg>")
open(out_svg, "w").write(svg)
print(len(p_pelo), "pelo", len(p_cara), "cara", len(svg) // 1024, "KB")
