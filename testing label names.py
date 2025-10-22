from ultralytics import YOLOvv8
model = YOLOvv8.from_pretrained("Ultralytics/YOLOv8")
source = 'http://images.cocodataset.org/val2017/000000039769.jpg'
model.predict(source=source, save=True)
