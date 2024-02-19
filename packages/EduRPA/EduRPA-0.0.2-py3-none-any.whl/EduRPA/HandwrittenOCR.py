from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import numpy as np
from PIL import Image
from robot.api.deco import keyword, not_keyword
import cv2
import json
class HandwrittenOCR:
    def __init__(self, lang, performance, *args, **kwargs):
        cfg = Cfg.load_config_from_name("vgg_seq2seq")
        cfg["device"] = "cpu"
        # cfg['weights'] = './weights/vgg_seq2seq.pth'
        vgg_seq2seq = Predictor(cfg)

        cfg = Cfg.load_config_from_name("vgg_transformer")
        # cfg['weights'] = './weights/vgg_transfer.pth'
        cfg["device"] = "cpu"
        vgg_transformer = Predictor(cfg)
        
        self.config = {
            "vi": {
              "fast": {
                "predictor": vgg_seq2seq
              },
              "accurate": {
                "predictor": vgg_transformer
              }
            },
            "en": {
                
            }
        }
        self.predictor = self.config[lang][performance]["predictor"]

    @not_keyword
    def image_preprocessing(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return thresh_image   
    
    @not_keyword
    def extract(self, images):
        predictor = self.predictor
        def predict(image):
            result = predictor.predict(Image.fromarray(image))
            return result
        results = []
        for image in images:
            print("Predict Image", image)
            prediction = predict(image)
            results.append(prediction)
        return results
    
    @keyword("Extract Text From Image Path")
    def detect(self, image_path, bounding_boxes):
        if(type (bounding_boxes) is str):
            bounding_boxes = json.loads(bounding_boxes)
        image = cv2.imread(image_path)
        extracted_images = []
        for bbox in bounding_boxes:
            x1, y1, x2, y2 = list(bbox)
            extracted_images.append(image[y1:y2, x1:x2])
        return self.extract(extracted_images)

    