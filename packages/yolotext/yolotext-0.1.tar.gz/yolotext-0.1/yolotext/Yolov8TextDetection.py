from ultralytics import YOLO
import torch
import warnings
import cv2
import os 
import gdown


class Yolov8TextDetection():
    def __init__(self, device="cuda"):
        self._device = device

        if not(torch.cuda.is_available()) and self._device == "cuda":
            warnings.warn("The device is set to cuda but there is no cuda device available. The algorithm will continue in cpu!!!")

        self._mdoel_ckpt_path = os.path.join(os.getcwd(), "weights", "yolov8_text.pt")

        if not(os.path.isfile(self._mdoel_ckpt_path)):
            os.makedirs(os.path.join(os.getcwd(), "weights"), exist_ok=True)
            gdown.download(
                    "https://drive.google.com/uc?id=1X8OVqXQ6ubsFV-nL4d1xmnKvXj2w5mFS",
                    self._mdoel_ckpt_path,
                    quiet=False
                    )
        

        try:
            self._model = YOLO(self._mdoel_ckpt_path)
        except Exception as e:
            print(e)

    def _process_predictions(self, raw_polylines, return_numpy=True):
        processed_polylines = []
        
        for polylines in raw_polylines:
            obbs = polylines.obb
            temp_polylines = []
            for obb in obbs:
                xyxyxyxy = obb.xyxyxyxy.to("cpu").numpy().astype(int)
                
                if not(return_numpy):
                    xyxyxyxy = xyxyxyxy.tolist()

                temp_polylines.append(xyxyxyxy)

            processed_polylines.append(temp_polylines)

        return processed_polylines
            

    def detect(self, images, confidence=0.5):
        polylines = self._model.predict(images, conf=confidence, verbose=True)
        polylines = self._process_predictions(polylines)

        return polylines
    
    def visualize_polylines(self, images, polylines_collection):
        visualized_images = []
        for img, polylines in zip(images, polylines_collection):
            for polyline in polylines:
                polyline = polyline.reshape((-1, 2))
                cv2.polylines(img,[polyline],True,(0,255,255),3)
            visualized_images.append(img)

        return visualized_images


