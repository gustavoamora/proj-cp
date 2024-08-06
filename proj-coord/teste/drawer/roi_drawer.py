# drawer/roi_drawer.py

import cv2

class ROIDrawer:
    def __init__(self, color=(0, 255, 0), thickness=2, font_scale=0.6, font=cv2.FONT_HERSHEY_SIMPLEX):
        self.color = color
        self.thickness = thickness
        self.font_scale = font_scale
        self.font = font

    def draw_roi(self, frame, roi, object_name):
        x, y, w, h = roi
        # Desenha o retângulo na ROI
        cv2.rectangle(frame, (x, y), (x+w, y+h), self.color, self.thickness)

        # Desenha o nome do objeto acima da ROI
        text_position = (x, y - 10)
        cv2.putText(frame, object_name, text_position, self.font, self.font_scale, self.color, self.thickness)
