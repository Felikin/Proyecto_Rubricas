def print_detection_result(detections):
    sum_persons = sum([1 for detection in detections if detection == "person"])

    if sum_persons >= len(detections) * 0.6:
        print("El profesor encendió la cámara")
