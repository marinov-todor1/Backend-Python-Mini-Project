# Interface for writing in the DB (probably singleton if the DB does not have auto-lock functionality)
import json
import numpy as np

db_dir = "./datasets.db"


# check if training dataset already exist with such name
def check_dataset_name(dataset_name, cursor):
    """ Validates if record with name X already exists in datasets table """
    query = "SELECT EXISTS(SELECT * FROM datasets WHERE name = ?)"
    parameters = (dataset_name,)
    cursor.execute(query, parameters)
    records = cursor.fetchall()
    return records[0][0]


def create_models_table_record(model_name, model_id, training_datasets, cursor):
    query = "INSERT OR IGNORE INTO models (name, training_datasets, model_id) VALUES (?, ?, ?)"
    parameters = (model_name, training_datasets, model_id)
    cursor.execute(query, parameters)


def create_datasets_table_record(name, size, type, cursor):
    query = "INSERT OR IGNORE INTO datasets(name, size, type) VALUES (?, ?, ?)"
    parameters = (name, size, type)
    cursor.execute(query, parameters)
    return cursor.lastrowid


def create_images_table(dataset_name, cursor):
    query1 = "CREATE TABLE IF NOT EXISTS "
    query2 = "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, bbox TEXT, " \
            "category_id TEXT, model_img_bbox TEXT, model_img_category TEXT, model_img_heatmap TEXT, " \
            "model_img_activations TEXT, dataset_name TEXT NOT NULL, model_id INTEGER NOT NULL, " \
            "FOREIGN KEY(dataset_name) REFERENCES datasets(name), FOREIGN KEY(model_id) REFERENCES models(model_id))"
    query = query1 + dataset_name + query2
    cursor.execute(query)
    # Only creates the table


def write_data_into_images_table(table_name, images, model_id, model_name, dataset_name, cursor):
    for img_info in images:
        query1 = "INSERT OR IGNORE INTO "
        query2 = "(name, bbox, category_id, model_img_bbox, model_img_category, model_img_heatmap, model_img_activations," \
                 "dataset_name, model_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        name = img_info.data()['name']

        # stringify all arrays/lists
        bbox = json.dumps(img_info.data()['img_bbox'])
        category_id = json.dumps(img_info.data()['img_category'])
        model_img_bbox = json.dumps(img_info.data()['model_image_bbox'])
        model_img_category = json.dumps(img_info.data()['model_image_category'])
        model_img_heatmap = np.array_str(img_info.data()['model_image_heatmap'])

        # First stringify all ndarrays in the list
        model_img_activations_temp = img_info.data()['model_image_activations']
        model_img_activations = []
        for activation in model_img_activations_temp:
            activation = np.array_str(activation, precision=None, suppress_small=True)
            model_img_activations.append(activation)
        # Now stringify the list itself
        model_img_activations = json.dumps(model_img_activations)

        # Save the query in the db
        query = query1 + table_name + query2
        parameters = (name, bbox, category_id, model_img_bbox, model_img_category, model_img_heatmap, model_img_activations, dataset_name, model_id)
        cursor.execute(query, parameters)
