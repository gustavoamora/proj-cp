# config/config.py

import json

class Config:
    def __init__(self, roi_file='data/rois.json'):
        # Carrega as ROIs do arquivo JSON
        with open(roi_file, 'r') as f:
            self.rois = json.load(f)

        # Nome dos objetos em cada ROI (exemplo, substitua pelos nomes reais)
        self.objects = {
            f"shelf_{i+1}": f"Item {chr(65+i)}" for i in range(len(self.rois))
        }

    def get_rois(self):
        return {f"shelf_{i+1}": tuple(roi) for i, roi in enumerate(self.rois)}

    def get_objects(self):
        return self.objects
