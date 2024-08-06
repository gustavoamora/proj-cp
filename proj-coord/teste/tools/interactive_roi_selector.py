import cv2
import json

class VideoROISelector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.rois = []
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.current_frame = None
        self.paused = False

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.end_point = (x, y)
                frame_copy = self.current_frame.copy()
                cv2.rectangle(frame_copy, self.start_point, self.end_point, (0, 255, 0), 2)
                cv2.imshow("Select ROIs", frame_copy)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_point = (x, y)
            roi = (self.start_point[0], self.start_point[1], self.end_point[0] - self.start_point[0], self.end_point[1] - self.start_point[1])
            self.rois.append(roi)
            print(f"ROI added: {roi}")

            # Draw the final rectangle on the current frame
            cv2.rectangle(self.current_frame, self.start_point, self.end_point, (0, 255, 0), 2)
            cv2.imshow("Select ROIs", self.current_frame)

    def select_rois(self):
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print(f"Erro: Não foi possível abrir o vídeo {self.video_path}")
            return

        cv2.namedWindow("Select ROIs")
        cv2.setMouseCallback("Select ROIs", self.draw_rectangle)

        while True:
            if not self.paused:
                ret, frame = cap.read()
                if not ret:
                    print("Fim do vídeo ou erro ao ler o vídeo.")
                    break
                self.current_frame = frame

            cv2.imshow("Select ROIs", self.current_frame)
            key = cv2.waitKey(30) & 0xFF

            # Pressione 'p' para pausar o vídeo
            if key == ord('p'):
                self.paused = not self.paused

            # Pressione 's' para salvar os ROIs e sair
            if key == ord('s'):
                self.save_rois()
                break

            # Pressione 'q' para sair sem salvar
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def save_rois(self, output_path='data/rois.json'):
        with open(output_path, 'w') as f:
            json.dump(self.rois, f)
        print(f"ROIs saved to {output_path}")

if __name__ == "__main__":
    video_path = "data/video.mp4"  # Caminho para o vídeo que você deseja usar
    selector = VideoROISelector(video_path)
    selector.select_rois()
