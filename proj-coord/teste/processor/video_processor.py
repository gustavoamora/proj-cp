# processor/video_processor.py

import cv2
from detector.interaction_detector import InteractionDetector
from drawer.roi_drawer import ROIDrawer
from counter.item_counter import ItemCounter

# Importe os detectores adicionais
from detector.optical_flow import OpticalFlowDetector
from detector.background_subtraction import BackgroundSubtractionDetector

class VideoProcessor:
    def __init__(self, config, detection_method='optical_flow'):
        self.config = config
        self.roi_drawer = ROIDrawer()
        self.item_counter = ItemCounter(config.get_rois())

        # Selecione o método de detecção com base na entrada
        if detection_method == 'optical_flow':
            self.detector = OpticalFlowDetector()
        elif detection_method == 'background_subtraction':
            self.detector = BackgroundSubtractionDetector()
        else:
            self.detector = InteractionDetector()  # Padrão

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Erro: Não foi possível abrir o vídeo {video_path}")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo ou erro ao ler o vídeo.")
                break

            frame_height, frame_width = frame.shape[:2]

            rois = self.config.get_rois()
            for shelf, roi in rois.items():
                x, y, w, h = roi

                if x < 0 or y < 0 or x+w > frame_width or y+h > frame_height:
                    print(f"Coordenadas da ROI para {shelf} estão fora dos limites do frame.")
                    continue

                roi_frame = frame[y:y+h, x:x+w]

                if roi_frame.size == 0:
                    print(f"ROI frame para {shelf} está vazio.")
                    continue

                interaction = self.detector.detect_interaction(roi_frame, shelf)
                if interaction:
                    object_name = self.config.get_objects()[shelf]
                    print(f"Interação detectada em {shelf}: {object_name}")
                    self.item_counter.increment(shelf)

                self.roi_drawer.draw_roi(frame, roi, self.config.get_objects()[shelf])

                count_text = f"Count: {self.item_counter.get_counts()[shelf]}"
                cv2.putText(frame, count_text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2.imshow('Gondola Monitoring', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
