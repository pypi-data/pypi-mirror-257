import  matplotlib.pyplot as plt
import cv2
import numpy as np
from .structures import CryoImageResults
from skimage import filters
import scipy

class Utils:
    @staticmethod
    def show_boxes(boxs, ax):
        for box in boxs:
            x0, y0 = box[0], box[1]
            w, h = box[2], box[3]
            ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=1))
    
    @staticmethod
    def show_annotation_boxes(boxs, ax):
        for box in boxs:
            x0, y0 = box[0] + 2, box[1] + 2
            w, h = box[2] - 2, box[3] - 2
            ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='red', facecolor=(0,0,0,0), lw=2))

    @staticmethod
    def show_annotation_points(points, ax):
        for point in points:
            x0, y0 = point[0], point[1]
            ax.plot(x0, y0, 'r+')
 
    #todo
    @staticmethod
    def visualize_detections(results: CryoImageResults, image, box_prompts = None, point_prompts = None, 
                          see_boxes = True, seepoint_prompts = None, see_masks = False, see_box_prompts = None,
                          annotation_boxes = None, annotation_points = None):
        # if image_scale_percent != 100:
        #     width = int(image.shape[1] * image_scale_percent / 100)
        #     height = int(image.shape[0] * image_scale_percent / 100)
        #     dim = (width, height)
        #     image = cv2.resize(image, dim)

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].imshow(image)
        ax[1].imshow(image)

        if annotation_boxes:
            Utils.show_annotation_boxes(annotation_boxes, ax[1])
        
        if annotation_points:
            Utils.show_annotation_points(annotation_points, ax[1])

        if see_masks:
            Utils.show_masks(results.segmentations, ax[1])
        


        if see_boxes:
            Utils.show_boxes(results.bounding_boxes, ax[1])

    
            
        #todo add support for prompts
        plt.show()
        return None
    
    #todo
    @staticmethod
    def show_masks(masks, axes=None):
     if axes:
        ax = axes
     else:
        ax = plt.gca()
        ax.set_autoscale_on(False)
     sorted_result = sorted(masks, key=(lambda x: x['area']), reverse=True)
     # Plot for each segment area
     for val in sorted_result:
        mask = val['segmentation']
        img = np.ones((mask.shape[0], mask.shape[1], 3))

        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            img[:,:,i] = color_mask[i]
            ax.imshow(np.dstack((img, mask*0.3)))
    
    @staticmethod
    def smooth_normalize_image(image_array, sigma):
        if (image_array.max() > 255 or image_array.min() < 0):
            image_array = filters.gaussian(image_array, sigma = sigma)
            zeroed_image = (image_array - image_array.min())
            pixel_intensity_range = (image_array.max() - image_array.min())
            image_array = (255.0 * zeroed_image / pixel_intensity_range).astype(np.uint8)
        return image_array
    
    @staticmethod
    def trim_by_area(targets, median_delta = 0.3):
        areas = targets.areas
        median = np.median(areas)
        average = np.average(areas)

        length = len(areas)

        for i in range(length):
            area = areas[length - i - 1]
            if abs(median - area) > (median_delta * median):
                targets.remove_idx(length - i - 1)
        return targets

    @staticmethod
    def visualize_image_segment(targets: CryoImageResults, index, ax):
        x0 = targets.bounding_boxes[index][0]
        x1 = targets.bounding_boxes[index][0] + targets.bounding_boxes[index][2]

        y0 = targets.bounding_boxes[index][1]
        y1 = targets.bounding_boxes[index][1] + targets.bounding_boxes[index][3]

        x0 = int(x0)
        x1 = int(x1)
        y0 = int(y0)
        y1 = int(y1)

        ax.imshow(targets.image[y0:y1, x0:x1])

    @staticmethod
    def generate_histogram(image, segmentation_mask):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        counts, bins = np.histogram(gray_image[segmentation_mask],  bins=256, range=(0, 255))
        return counts, bins
    