import json
import os
from dataclasses import dataclass

import numpy as np
import supervision as sv
import torch
from autodistill.detection import CaptionOntology, DetectionBaseModel
from ultralytics import YOLOWorld

HOME = os.path.expanduser("~")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@dataclass
class YoloWorld(DetectionBaseModel):
    ontology: CaptionOntology

    def __init__(self, ontology: CaptionOntology, model_type: str = "yolov8s-world.pt"):
        self.ontology = ontology
        self.model = YOLOWorld(model_type)
        self.model.to(DEVICE)
        labels = self.ontology.prompts()
        self.model.set_classes(labels)

    def predict(self, input: str, confidence=0.1) -> sv.Detections:
        with torch.no_grad():
            outputs = self.model(input)
            # 0 as there is only one image
            outputs = json.loads(outputs[0].tojson())
            boxes, labels, scores = [], [], []
            # filter with score < confidence
            for output in outputs:
                if output["confidence"] > confidence:
                    box = output["box"]
                    boxes.append([box[key] for key in ("x1", "y1", "x2", "y2")])
                    labels.append(output["class"])
                    scores.append(output["confidence"])

            if len(boxes) == 0:
                return sv.Detections.empty()

            detections = sv.Detections(
                xyxy=np.array(boxes),
                class_id=np.array(labels),
                confidence=np.array(scores),
            )

            return detections
