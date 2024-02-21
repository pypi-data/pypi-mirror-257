import numpy as np

class CryoImageResults:
    def __init__(self, image, masks):
        self.image = image
        #self.full_image_histogram = []
        self.bounding_boxes = []
        self.histograms = []
        self.areas = []
        self.segmentations = []

        for mask in masks: 
            self.bounding_boxes.append(mask['bbox'])
            self.areas.append(mask['area'])
            self.segmentations.append(mask['segmentation'])
            self.histograms.append(np.histogram(image[mask['segmentation']], bins=256, range=(0, 255)))

    def remove_idx(self, idx):
        del self.bounding_boxes[idx]
        del self.histograms[idx]
        del self.areas[idx]
        del self.segmentations[idx]

    def __len__(self):
        return len(self.segmentations)
    
    