# detector/cnn_object_detection.py

import cv2
import numpy as np

class CNNObjectDetector:
    def __init__(self, config_path, weights_path, names_path, confidence_threshold=0.5, nms_threshold=0.4):
        # Carrega a rede neural do YOLOv3
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        # Carrega os nomes das classes
        with open(names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold

    def detect_interaction(self, frame, roi):
        # Prepara a imagem da ROI para a rede neural
        x, y, w, h = roi
        roi_frame = frame[y:y+h, x:x+w]

        blob = cv2.dnn.blobFromImage(roi_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        # Processa as saídas da rede neural
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > self.confidence_threshold:
                    # Calcula as coordenadas da caixa delimitadora
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    width = int(detection[2] * w)
                    height = int(detection[3] * h)

                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)

                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Aplica supressão de não-máximos
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)

        # Verifica se houve alguma detecção de objeto
        for i in indices:
            i = i[0]
            box = boxes[i]
            x, y, w, h = box
            label = str(self.classes[class_ids[i]])
            print(f"Objeto detectado: {label} com confiança de {confidences[i] * 100:.2f}%")

            # Desenha a caixa delimitadora e o rótulo na imagem
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(roi_frame, f"{label}: {int(confidences[i] * 100)}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Retorna True se qualquer objeto foi detectado
        return len(indices) > 0
