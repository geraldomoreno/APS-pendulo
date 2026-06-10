import cv2
import numpy as np
import csv

# === CONFIGURAÇÕES ===
VIDEO_PATH = r"C:\Users\Casa\Downloads\trabalho_pendulo\oscilando.mp4"
OUTPUT_CSV = r"C:\Users\Casa\Downloads\trabalho_pendulo\posicoes.csv"

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"FPS do vídeo: {fps}")

# Vermelho no HSV aparece em dois ranges
LOWER1 = np.array([0, 80, 50])
UPPER1 = np.array([12, 255, 255])
LOWER2 = np.array([170, 80, 50])
UPPER2 = np.array([180, 255, 255])

MAX_SALTO = 35  # pixels — ajusta se o tomate se mover muito rápido entre frames

positions = []
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    ROI_Y_MIN = 0
    ROI_Y_MAX = 800  # ajusta esse valor — corta antes do móvel aparecer

    frame_roi = frame.copy()
    frame_roi[ROI_Y_MAX:, :] = 0  # zera tudo abaixo da ROI (vira preto)

    hsv = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

    # Combina os dois ranges do vermelho
    mask1 = cv2.inRange(hsv, LOWER1, UPPER1)
    mask2 = cv2.inRange(hsv, LOWER2, UPPER2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Suavização mais agressiva
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=5)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)

        # Ignora contornos pequenos (ruído)
        if cv2.contourArea(c) < 300:
            frame_num += 1
            continue

        x_caixa, y_caixa, w, h = cv2.boundingRect(c)
        cx = int(x_caixa + (w / 2))
        cy = int(y_caixa + (h / 2))

        # Descarta frames com salto absurdo em relação ao frame anterior
        if positions:
            ultimo_cx, ultimo_cy = positions[-1][2], positions[-1][3]
            distancia = np.sqrt((cx - ultimo_cx)**2 + (cy - ultimo_cy)**2)
            if distancia > MAX_SALTO:
                frame_num += 1
                continue

        t = frame_num / fps
        positions.append((frame_num, t, cx, cy))

        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        cv2.rectangle(frame, (x_caixa, y_caixa), (x_caixa + w, y_caixa + h), (255, 0, 0), 1)

    cv2.imshow("Rastreamento", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

    frame_num += 1

cap.release()
cv2.destroyAllWindows()

with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["frame", "t(s)", "x(px)", "y(px)"])
    for pos in positions:
        f_num, t_sec, cx, cy = pos
        writer.writerow([f_num, round(t_sec, 3), cx, cy])

print(f"Salvo {len(positions)} posições em {OUTPUT_CSV}")