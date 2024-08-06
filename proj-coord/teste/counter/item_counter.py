# item_counter.py

class ItemCounter:
    def __init__(self, rois):
        # Inicializa um dicionário para manter a contagem de interações por ROI
        self.counts = {shelf: 0 for shelf in rois}

    def increment(self, roi_name):
        # Incrementa a contagem para a ROI especificada
        if roi_name in self.counts:
            self.counts[roi_name] += 1
            print(f"Interação contada em {roi_name}: total agora é {self.counts[roi_name]}")

    def get_counts(self):
        # Retorna o dicionário de contagens
        return self.counts
