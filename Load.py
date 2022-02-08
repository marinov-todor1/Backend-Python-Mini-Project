import os
import json

from model_data import DummyModel


class LoadImgMetadata():
    """ Collects image metadata from external datasets """
    def __init__(self, image_name, dataset_directory):
        # test for empty directories and incorrect naming
        if len(os.listdir(dataset_directory)) == 0:
            raise "Provided directory is empty"
        elif "images" not in os.listdir(dataset_directory):
            raise "No 'images' folder was found"
        elif "annotations" not in os.listdir(dataset_directory):
            raise "No 'annotations' folder was found"

        self.img_name = image_name
        self.img_folder = os.path.join(dataset_directory, "images")
        self.annotations_folder = os.path.join(dataset_directory, "annotations")

        if len(self.img_folder) == 0:
            raise "No image files were found in 'images' folder"
        elif len(os.listdir(self.annotations_folder)) == 0 or len(os.listdir(self.annotations_folder)) != len(os.listdir(self.img_folder)):
            raise "No annotation files were found in 'annotations' folder or their count does not match the image count"
        elif self.img_name not in os.listdir(self.img_folder):
            raise f"No image was found with name: {self.img_name}"

    def load_img_bbox(self):
        # Compute the path to the annotations directory
        annotations_img_path = os.path.abspath(os.path.join(self.annotations_folder, self.img_name))
        annotations_img_path = os.path.splitext(annotations_img_path)[0] + ".json"
        # Load the annotations data
        with open(annotations_img_path, "r") as annotations_file:
            img_data = json.load(annotations_file)
        bbox_data = img_data['bbox']
        return bbox_data

    def load_img_category(self):
        # Compute the path to the annotations directory
        annotations_img_path = os.path.abspath(os.path.join(self.annotations_folder, self.img_name))
        annotations_img_path = os.path.splitext(annotations_img_path)[0] + ".json"
        # Load the annotations data
        with open(annotations_img_path, "r") as annotations_file:
            img_data = json.load(annotations_file)
        category_id = img_data['category_id']
        return category_id

    def load_all_metadata(self):
        all_data = {'name': self.img_name, 'image_bbox': self.load_img_bbox(),
                    'image_category': self.load_img_category()}
        return all_data


class LoadImgModelData():
    """ Generates models metadata from external datasets"""
    def __init__(self, image_name, dataset_directory, model_id):
        # test for empty directories and incorrect naming
        if len(os.listdir(dataset_directory)) == 0:
            raise "Provided directory is empty"
        elif "images" not in os.listdir(dataset_directory):
            raise "No 'images' folder was found"
        elif "annotations" not in os.listdir(dataset_directory):
            raise "No 'annotations' folder was found"

        self.img_folder = os.path.join(dataset_directory, "images")
        self.img_path = os.path.join(dataset_directory, "images", image_name)
        self.model = model_id

        if len(self.img_folder) == 0:
            raise "No image files were found in 'images' folder"
        elif image_name not in os.listdir(self.img_folder):
            raise f"No image was found with the provided name: {image_name}"

    def generate_bbox_and_category_id(self):
        model_prediction = DummyModel(self.model).get_model_prediction(self.img_path)
        return model_prediction

    def generate_heatmap(self):
        model_heatmap = DummyModel(self.model).get_img_heatmap(self.img_path)
        return model_heatmap

    def generate_activations(self):
        model_activations = DummyModel(self.model).get_img_activations(self.img_path)
        return model_activations

    def get_all_model_data(self):
        bbox_category = self.generate_bbox_and_category_id()
        all_data = {"bbox": bbox_category['bbox'], "category_id": bbox_category['category_id'],
                    "heatmap": self.generate_heatmap(), "activations": self.generate_activations()}
        return all_data