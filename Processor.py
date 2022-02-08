import os
from DataObjects import Image, Model, Dataset
from model_data import get_models
from Load import LoadImgMetadata, LoadImgModelData
import Writer
import sqlite3

db_dir = "./datasets.db"
datasets_dir = "./dataset_data/"
single_dataset_dir = "./dataset_data/human_dataset"


def get_dataset_paths(datasets_dir):
    """" Compute folder structure and naming """

    # find images, annotations and dataset folders in arbitrary folder structure
    if not os.path.exists(datasets_dir):
        raise f"The directory does not exist -> {datasets_dir}"

    datasets = []
    # explore folder tree and extract links to images, annotations and dataset folders
    for (root, dir, file) in os.walk(datasets_dir, topdown=False):

        if len(file) != 0:
            file_extension = os.path.splitext(file[0])[1]
        else:
            continue

        # compute dataset information (name, path, img_path, annotations_path) based on images folder
        if file_extension == ".jpg":
            img_path = os.path.abspath(root)
            current_dataset_path = os.path.abspath(os.path.join(root, os.pardir))
            annotation_path = os.path.join(current_dataset_path, "annotations")
            dataset_name = os.path.basename(current_dataset_path)
            dataset = {"name": dataset_name, "dataset_dir": current_dataset_path, "img_dir": img_path,
                       "annotations_dir": annotation_path}
            datasets.append(dataset)
            if not os.path.exists(annotation_path):
                raise f"No 'annotations' folder in {current_dataset_path}"

    return datasets


def generate_dataset_info(dataset_name, dataset_dir, img_dir):
    """ Load the provided dataset and collect metadata """

    # collect all datasets metadata
    dataset_size = len(os.listdir(img_dir))
    dataset_type = os.path.splitext(os.listdir(img_dir)[0])[1]
    dataset = Dataset()
    dataset.record_dataseet_metadata(dataset_name, dataset_size, dataset_type)

    # collect models data
    models_info = generate_model_info()

    # collect all image data
    images_info = {}
    for model in models_info:
        images = generate_image_info(dataset_dir, model.data()['id'])
        images_info[model.data()['name']] = images

    dataset_all_info = {"dataset_info": dataset, "models_info": models_info, "images_info": images_info}
    return dataset_all_info


def generate_model_info():
    """ Load active models from the provided file and collect metadata"""

    # collect all models metadata
    models = get_models()
    models_data = []
    for model in models:
        name = model.model_name
        datasets = model.model_datasets
        model_id = model.model_id
        new_model = Model()
        new_model.record_model_metadata(name, model_id, datasets)
        models_data.append(new_model)

        # collect all img data
        # generate_image_info(dataset_dir, model_id)

    return models_data


def generate_image_info(dataset_dir, model_id):
    """ Load image and annotation files from directory and collect meta"""

    images_data = []

    # compute all image names
    img_dir = os.path.join(dataset_dir, "images")
    images_for_dataset = os.listdir(img_dir)

    # compute all image and model_image metadata
    for img in images_for_dataset:
        img_meta = LoadImgMetadata(img, dataset_dir).load_all_metadata()
        img_model_meta = LoadImgModelData(img, dataset_dir, model_id).get_all_model_data()
        image = Image()
        image.record_img_metadata(img_meta["name"], img_meta["image_bbox"], img_meta["image_category"])
        image.record_model_img_metadata(img_model_meta["bbox"], img_model_meta["category_id"],
                                        img_model_meta["heatmap"], img_model_meta["activations"])
        images_data.append(image)

    return images_data


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

    return connection


def main():

    # Import all datasets data from provided directory

    # Compute all datasets paths
    datasets_paths = get_dataset_paths(datasets_dir)
    # Open a connection with the database
    connection = sqlite3.connect(db_dir)
    cursor = connection.cursor()

    # Check if datasets names already exist and record them into the db
    for dataset in datasets_paths:
        dataset_name = dataset['name']
        if Writer.check_dataset_name(dataset_name, cursor):
            continue
            raise Exception(f"A record with name {dataset_name} already exists in table routing_table")

    # Generate all datasets data for DB import
    datasets_info = []
    for dataset in datasets_paths:
        dataset_info = generate_dataset_info(dataset['name'], dataset['dataset_dir'], dataset['img_dir'])
        datasets_info.append(dataset_info)

    # Save the datasets name in the routing_table
    # TODO #Add BEGIN TRANSACTION
    for dataset in datasets_paths:
        name = dataset['name']
        Writer.create_routing_table_record(name, cursor)

    # Update Models table with the respective data
    models = datasets_info[0]['models_info']
    for model in models:
        model_name = model.data()['name']
        model_id = model.data()['id']
        model_datasets = ",".join(model.data()['datasets'])
        Writer.create_models_table_record(model_name, model_id, model_datasets, cursor)

    # Update Datasets table with the respective data
    for record in datasets_info:
        dataset_info = record['dataset_info'].data()
        name = dataset_info['name']
        size = dataset_info['size']
        type = dataset_info['type']
        Writer.create_datasets_table_record(name, size, type, cursor)

    # Create 'dataset_name'_Images tables for each model
    for dataset in datasets_info:
        for model in dataset['models_info']:
            # create img_table Datasetname_Modelname_Images

            # for img in dataset['images_info'][model.data()['name']
                # insert rows in img_table
            pass



        # Save all image data inside

    connection.commit()








if __name__ == "__main__":
    main()
