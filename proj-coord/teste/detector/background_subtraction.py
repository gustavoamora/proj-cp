# detector/background_subtraction.py

import cv2

class BackgroundSubtractionDetector:
    def __init__(self):
        self.back_sub = cv2.createBackgroundSubtractorMOG2()

    def detect_interaction(self, frame, roi):
        # Aplicar subtração de fundo para detectar movimento
        fg_mask = self.back_sub.apply(frame)

        # Determine a interação com base na quantidade de pixels em movimento
        return cv2.countNonZero(fg_mask) > 100  # Ajuste o limiar conforme necessário
