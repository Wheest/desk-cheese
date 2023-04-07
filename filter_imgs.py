#!/usr/bin/env python3
import cv2
import os
import numpy as np
from tqdm import tqdm
import urllib.request


def download_yolo_files():
    os.makedirs("yolov3", exist_ok=True)

    base_url = "https://github.com/pjreddie/darknet/raw/master/"
    files = ["cfg/yolov3.cfg", "data/coco.names"]
    weights_url = "https://pjreddie.com/media/files/yolov3.weights"

    for file in files:
        file_url = base_url + file
        destination_file = os.path.join("yolov3", os.path.basename(file))

        if not os.path.exists(destination_file):
            print(f"Downloading '{file}' from '{file_url}'...")
            urllib.request.urlretrieve(file_url, destination_file)
            print(f"Downloaded '{file}' as '{destination_file}'")

    destination_weights = os.path.join("yolov3", os.path.basename(weights_url))

    if not os.path.exists(destination_weights):
        print(f"Downloading 'yolov3.weights' from '{weights_url}'...")
        urllib.request.urlretrieve(weights_url, destination_weights)
        print(f"Downloaded 'yolov3.weights' as '{destination_weights}'")


def load_yolo_model(weights_file, config_file, class_labels_file):
    # Load the YOLO model
    net = cv2.dnn.readNet(weights_file, config_file)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
    with open(class_labels_file, "rt") as f:
        class_names = f.read().rstrip("\n").split("\n")
    return net, class_names


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def load_pre_sifted_data(base_path: os.PathLike):
    human_images, non_human_images = [], []

    # load human images
    f = os.path.join(base_path, "human.txt")
    if os.path.exists(f):
        with open(f) as file:
            while line := file.readline():
                human_images.append(line.rstrip())

    # load non-human images
    f = os.path.join(base_path, "non_human.txt")
    if os.path.exists(f):
        with open(f) as file:
            while line := file.readline():
                non_human_images.append(line.rstrip())

    return human_images, non_human_images


def dump_sift_data(base_path, human_images, non_human_images):
    human_images = sorted(human_images)
    non_human_images = sorted(non_human_images)

    # save human images
    f = os.path.join(base_path, "human.txt")
    print(f"we have {len(human_images)} human_images")
    with open(f, "w") as f:
        for d in human_images:
            f.write(f"{d}\n")

    # load non-human images
    print(f"we have {len(non_human_images)} non_human_images")
    f = os.path.join(base_path, "non_human.txt")
    with open(f, "w") as f:
        for d in non_human_images:
            f.write(f"{d}\n")


def sift_human_images(images_directory, yolo_weights, yolo_config, yolo_classes):
    net, class_names = load_yolo_model(yolo_weights, yolo_config, yolo_classes)

    human_images, non_human_images = load_pre_sifted_data(images_directory)

    for image_name in tqdm(os.listdir(images_directory)):
        if not image_name.endswith(".jpg"):
            continue

        # check if we have already processed this image, e.g. from the cache
        if image_name in human_images or image_name in non_human_images:
            continue

        image_path = os.path.join(images_directory, image_name)
        image = cv2.imread(image_path)
        height, width, channels = image.shape

        # Detect objects in the image
        blob = cv2.dnn.blobFromImage(
            image, 0.00392, (416, 416), (0, 0, 0), True, crop=False
        )
        net.setInput(blob)
        outs = net.forward(get_output_layers(net))

        # Iterate through the detected objects
        human = False
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_names[class_id] == "person":
                    human_images.append(image_name)
                    human = True
                    break

        if not human:
            non_human_images.append(image_name)

    dump_sift_data(images_directory, human_images, non_human_images)
    return human_images, non_human_images


if __name__ == "__main__":
    images_directory = "./pics/"

    yolo_weights = "yolov3/yolov3.weights"
    yolo_config = "yolov3/yolov3.cfg"
    yolo_classes = "yolov3/coco.names"

    download_yolo_files()

    # Run the function and get a list of images containing humans
    human_images_list, non_human_images_list = sift_human_images(
        images_directory, yolo_weights, yolo_config, yolo_classes
    )
