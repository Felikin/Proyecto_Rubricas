from tqdm import tqdm


def print_detection_result(detections, model):
    names = model.names
    sum = 0 
    for detection in tqdm(detections, desc="Procesando video"):
        for class_name in detection.boxes.cls:
            if names[int(class_name)] == "person":
                sum += 1

    if sum >= len(detections) * 0.6:
        print("El profesor encendió la cámara")
