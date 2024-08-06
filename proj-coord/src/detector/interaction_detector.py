# detector/interaction_detector.py

import cv2

class InteractionDetector:
    def __init__(self):
        # Inicialize qualquer parâmetro necessário
        self.previous_frames = {}

    def detect_interaction(self, roi_frame, roi_name):
        # Converte o frame para escala de cinza
        gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
        
        # Aplica uma técnica de detecção simples, como a detecção de movimento
        if roi_name not in self.previous_frames:
            self.previous_frames[roi_name] = gray_frame
            return False

        # Calcula a diferença entre o frame atual e o anterior
        frame_delta = cv2.absdiff(self.previous_frames[roi_name], gray_frame)
        _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)

        # Detectar contornos para identificar movimentos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Atualiza o frame anterior
        self.previous_frames[roi_name] = gray_frame

        # Verifica se algum contorno é significativo para considerar como interação
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Ajuste o valor conforme necessário
                return True

        return False
