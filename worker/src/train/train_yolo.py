from ultralytics import YOLO

# Load a pre model
model = YOLO("yolov8n.pt")
# Train the model
results = model.train(
    data="Worker-Safety.v1i.yolov8/data.yaml",
    epochs=100,
    batch=4,
    imgsz=416,
    workers=2,
    device=0
)