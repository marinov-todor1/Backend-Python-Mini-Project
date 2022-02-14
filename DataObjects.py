class Image:
    """ Internal representation of image metadata """
    def __init__(self):
        self._img_name = ""
        self._img_bbox = []
        self._img_category = []
        self._model_image_bbox = {}
        self._model_image_category = {}
        self._model_image_heatmap = {}
        self._model_image_activations = {}
        self._model_id = {}
        self._dataset_name = {}

        self._aggregated_data = {"name": self._img_name, "img_bbox": self._img_bbox, "img_category": self._img_category,
                           "model_image_bbox": self._model_image_bbox, "model_image_category": self._model_image_category,
                           "model_image_heatmap": self._model_image_heatmap,
                           "model_image_activations": self._model_image_activations, "dataset_name": self._dataset_name, "model_id": self._model_id}

    def record_img_metadata(self, name, bbox, category, dataset_name, model_id):
        # check if name is compliant -> for example, contains the file extension (or not) # TODO
        self._aggregated_data["name"] = name

        # check if bbox is compliant with internal format, type, etc. before implementing #TODO
        self._aggregated_data["img_bbox"] = bbox

        # check if category is compliant -> for example is integer, in range of (a, b) #TODO
        self._aggregated_data["img_category"] = category

        # save dataset_name
        self._aggregated_data["dataset_name"] = dataset_name

        # save model_id
        self._aggregated_data["model_id"] = model_id

    def record_model_img_metadata(self, model_img_bbox, model_img_category, heatmap, activations):
        # check if bbox is compliant with internal format, type, etc. before implementing #TODO
        self._aggregated_data["model_image_bbox"] = model_img_bbox

        # check if category is compliant -> for example is integer, in range of (a, b) #TODO
        self._aggregated_data["model_image_category"] = model_img_category

        # check if bbox is compliant with internal format, type, etc. before implementing #TODO
        self._aggregated_data["model_image_heatmap"] = heatmap

        # check if bbox is compliant with internal format, type, etc. before implementing #TODO
        self._aggregated_data["model_image_activations"] = activations

    def data(self):
        return self._aggregated_data


class Model:
    """ Internal representation of model metadata """
    def __init__(self):
        self._name = "none"
        self._id = -1
        self._datasets = "none"
        self._aggregated_data = {"name": self._name, "id": self._id, "datasets": self._datasets}

    def record_model_metadata(self, name, id, datasets):
        # check if model with the same name and/or id already exists before implementing #TODO
        self._aggregated_data["name"] = name
        self._aggregated_data["id"] = id
        self._aggregated_data["datasets"] = datasets

    def data(self):
        return self._aggregated_data


class Dataset:
    """ Internal representation of dataset metadata """
    def __init__(self):
        self._name = ""
        self._size = 0
        self._type = ""
        self._aggregated_data = {"name": self._name, "size": self._size, "type": self._type}

    def record_dataseet_metadata(self, name, size, type):
        # check if dataset with that name already exist and the image type is supported #TODO
        self._aggregated_data["name"] = name
        self._aggregated_data["size"] = size
        self._aggregated_data["type"] = type

    def data(self):
        return self._aggregated_data