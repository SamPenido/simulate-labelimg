import cv2
import os
import time

# Configurações
video_path = "/home/bruno/live/output.avi"
output_images = "dataset/images"
output_labels = "dataset/labels"
os.makedirs(output_images, exist_ok=True)
os.makedirs(output_labels, exist_ok=True)

# Pega o nome do vídeo sem a extensão
video_name = os.path.splitext(os.path.basename(video_path))[0]

# Variáveis globais
bboxes = []
drawing = False
ix, iy = -1, -1
speed = 1.0  # Velocidade inicial
frame_pos = 0

# Função para normalizar coordenadas para YOLO
def normalize_bbox(x1, y1, x2, y2, width, height):
    # Garante que x1, y1 sejam sempre o canto superior esquerdo
    x1, x2 = sorted([x1, x2])  
    y1, y2 = sorted([y1, y2])

    x_center = (x1 + x2) / 2 / width
    y_center = (y1 + y2) / 2 / height
    w = abs(x2 - x1) / width
    h = abs(y2 - y1) / height
    return x_center, y_center, w, h

# Callback do mouse para desenhar a BBox
def draw_bbox(event, x, y, flags, param):
    global ix, iy, drawing, bboxes
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, x2 = sorted([ix, x])  # Corrige inversão de X
        y1, y2 = sorted([iy, y])  # Corrige inversão de Y
        bboxes.append([x1, y1, x2, y2, -1])  # Classe indefinida (-1)

# Captura de vídeo
cap = cv2.VideoCapture(video_path)
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", draw_bbox)

while cap.isOpened():
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
    ret, frame = cap.read()
    if not ret:
        break
    
    original_frame = frame.copy()
    height, width, _ = frame.shape
    
    # Desenha BBoxes na tela
    for bbox in bboxes:
        x1, y1, x2, y2, cls = bbox
        color = (0, 255, 0) if cls == -1 else (255, 0, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        if cls != -1:
            cv2.putText(frame, str(cls), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow("Video", frame)
    key = cv2.waitKey(int(1000 / 30 / speed)) & 0xFF  
    
    if key == ord('q'):
        break
    elif key == ord('n'):  # Resetar BBox
        bboxes = []
    elif key == 8:  # Tecla Del
        bboxes = []
    elif key == ord('s'):  # Salvar frame e anotações
        timestamp = int(time.time())

        # Adiciona o nome do vídeo no início do nome do arquivo
        frame_name = f"{video_name}_frame_{frame_pos}_{timestamp}.jpg"
        txt_name = f"{video_name}_frame_{frame_pos}_{timestamp}.txt"

        # Salvar imagem
        cv2.imwrite(os.path.join(output_images, frame_name), original_frame)
        
        with open(os.path.join(output_labels, txt_name), "w") as f:
            for bbox in bboxes:
                x1, y1, x2, y2, cls = bbox
                if cls != -1:
                    norm_bbox = normalize_bbox(x1, y1, x2, y2, width, height)
                    f.write(f"{cls} {' '.join(map(str, norm_bbox))}\n")
                    
    elif key in [ord(str(i)) for i in range(6)]:  # Classificação
        for bbox in bboxes:  # Mantém todas as BBoxes e só altera a classe
            bbox[4] = int(chr(key))
    elif key == ord('+') and speed < 2.0:
        speed += 0.25
    elif key == ord('-') and speed > 0.5:
        speed -= 0.25
    elif key == ord('a'):  # Seta esquerda (retroceder 5s)
        frame_pos = max(0, frame_pos - 150)
    elif key == ord('d'):  # Seta direita (avançar 5s)
        frame_pos += 150
    else:
        frame_pos += 1  

cap.release()
cv2.destroyAllWindows()
