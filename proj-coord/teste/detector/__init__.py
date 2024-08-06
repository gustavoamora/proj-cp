# detector/__init__.py

from .interaction_detector import InteractionDetector
from .optical_flow import OpticalFlowDetector
from .background_subtraction import BackgroundSubtractionDetector
#from .cnn_object_detection import CNNObjectDetector
#from .object_tracking import ObjectTrackingDetector

__all__ = [
    'InteractionDetector',
    'OpticalFlowDetector',
    'BackgroundSubtractionDetector',
    #'CNNObjectDetector',
    #'ObjectTrackingDetector'
]
