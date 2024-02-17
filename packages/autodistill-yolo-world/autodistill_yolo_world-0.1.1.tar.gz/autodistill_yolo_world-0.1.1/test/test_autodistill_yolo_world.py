import os

from autodistill.detection import CaptionOntology

from autodistill_yolo_world.yolo_world import YoloWorld


def test_YoloWorld():
    caption_ontology = CaptionOntology({"person": "person", "car": "car"})
    yolo_world = YoloWorld(ontology=caption_ontology)
    input_image = os.path.join("assets", "test.jpg")
    detections = yolo_world.predict(input_image)
    assert len(detections.xyxy) == 8
    assert len(detections.class_id) == 8
    assert len(detections.confidence) == 8
