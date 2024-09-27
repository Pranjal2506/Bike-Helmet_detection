import base64
import numpy as np
import cv2
from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO("model.pt")  # Load your trained YOLO model
classNames = ["No_Helmet", "Helmet"]  # Define class names

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    global cls
    data = request.get_json()
    image_data = data['image']

    # Process the image data (strip out the header)
    header, encoded = image_data.split(',', 1)
    decoded_image = base64.b64decode(encoded)

    # Convert the image data to a NumPy array for processing
    np_image = np.frombuffer(decoded_image, np.uint8)
    img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Run the machine learning model on the image
    results = model(img)[0]
    cls = 0  # Default class (No Helmet)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)  # Draw rectangle
            cls = int(box.cls[0])  # Get the class of the detected object
            org = (x1, y1)
            cv2.putText(img, classNames[cls], org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Convert processed image back to base64
    _, buffer = cv2.imencode('.png', img)
    processed_image_data = base64.b64encode(buffer).decode('utf-8')

    # Determine alert message
    alert_message = "Helmet detected!" if cls == 1 else "No Helmet detected!"

    return jsonify({
        "image": f"data:image/png;base64,{processed_image_data}",
        "alert": alert_message,
        "prediction": cls  # Include the class prediction in the response
    })