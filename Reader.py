import json
import numpy as np
import sqlite3
from DataObjects import Image, Dataset, Model

db_dir = "./datasets.db"


def read_img_data(dataset_name, model_name, name, cursor):
    """ Retrieve the image data from the requested table """
    query1 = "SELECT * FROM "
    table_name = f"{dataset_name}_{model_name} WHERE name = ?"
    query = query1 + table_name
    param = (name, )
    data = cursor.execute(query, param)
    data = data.fetchall()

    name = data[0][1]
    bbox = json.loads(data[0][2])
    category_id = json.loads(data[0][3])
    model_img_bbox = json.loads(data[0][4])
    model_img_category = json.loads(data[0][5])

    # TODO find a way to properly retrieve the array from string - np.frombuffer((data[0][6]).encode(), dtype=np.uint8)
    model_img_heatmap = data[0][6]

    activations_temp = json.loads(data[0][7])

    # TODO find a way to properly retrieve the array from string
    model_img_activations = []
    for activation in activations_temp:
        activation = np.frombuffer(activation.encode(), dtype=np.uint8)
        model_img_activations.append(activation)

    model_id = data[0][9]
    image = Image()
    image.record_img_metadata(name, bbox, category_id, dataset_name, model_id)
    image.record_model_img_metadata(model_img_bbox, model_img_category, model_img_heatmap, activations_temp) # TODO change activations_temp to model_img_activations once string conversion is complete
    return image


def read_dataset_data(dataset_name, cursor):
    query = "SELECT * FROM datasets WHERE name = ?"
    param = (dataset_name, )
    data = cursor.execute(query, param)
    data = data.fetchall()

    name = data[0][0]
    size = data[0][1]
    type = data[0][2]
    dataset = Dataset()
    dataset.record_dataseet_metadata(name, size, type)
    return dataset


def read_model_data(model_name, cursor):
    query = "SELECT * FROM models WHERE name = ?"
    param = (model_name,)
    data = cursor.execute(query, param)
    data = data.fetchall()

    name = data[0][0]
    training_datasets = data[0][1]
    model_id = data[0][2]
    model = Model()
    model.record_model_metadata(name, model_id, training_datasets)
    return model