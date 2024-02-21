from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry
from .structures import *
from .utils import *

class Csam:
    def __init__(self, model_name, model_checkpoint, device = "cuda"):
        self.model = model_name
        self.checkpoint = model_checkpoint
        self.device = device

        self.__load_model()

    def __load_model(self):
        sam = sam_model_registry[self.model](checkpoint = self.checkpoint)
        sam.to(self.device)

        self.mask_generator = SamAutomaticMaskGenerator(sam)
        self.predictor = SamPredictor(sam)   

    def square_finder(self, image, point_prompts = None, box_prompts = None):
        image = Utils.smooth_normalize_image(image, 1)

        if not box_prompts or point_prompts:
            masks = self.mask_generator.generate(image)
            results = CryoImageResults(image, masks)
            results = Utils.trim_by_area(results, 2.5)

        #todo add support for prompts
        return results
    
    def hole_finder(self, image, point_prompts = None, box_prompts = None):
        image = Utils.smooth_normalize_image(image, 1)

        if not box_prompts or point_prompts:
            masks = self.mask_generator.generate(image)
            results = CryoImageResults(image, masks)
            results = Utils.trim_by_area(results, 2.0)

        #todo add support for prompts
        return results

