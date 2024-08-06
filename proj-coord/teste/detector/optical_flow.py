# detector/optical_flow.py

import cv2
import numpy as np

class OpticalFlowDetector:
    def __init__(self):
        self.prev_frame = None

    def detect_interaction(self, frame, roi):
        if self.prev_frame is None:
            self.prev_frame = frame
            return False

        # Calcule o fluxo óptico entre o frame atual e o anterior
        flow = cv2.calcOpticalFlowFarneback(self.prev_frame, frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Calcule a magnitude e a direção do fluxo
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Atualize o frame anterior
        self.prev_frame = frame

        # Determine a interação com base na magnitude do fluxo
        return np.mean(magnitude) > 2.0  # Ajuste o limiar conforme necessário
