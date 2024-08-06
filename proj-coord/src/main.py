# main.py

from config.config import Config
from processor.video_processor import VideoProcessor

def main():
    config = Config()

    # Selecione a técnica de detecção a ser usada
    detection_method = 'deafult'  # ou 'background_subtraction', 'default', etc.

    processor = VideoProcessor(config, detection_method=detection_method)

    video_path = "data/video.mp4"  # Atualize com o caminho para o seu vídeo
    processor.process_video(video_path)

if __name__ == "__main__":
    main()
