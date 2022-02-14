import os
from DataObjects import Image, Model, Dataset
from model_data import get_models
from Load import LoadImgMetadata, LoadImgModelData
import Writer
import sqlite3
import itertools


single_dataset_dir = "./dataset_data/human_dataset"


def get_dataset_paths(datasets_dir):
    """" Compute folder structure and naming """

    # find images, annotations and dataset folders in arbitrary folder structure
    if not os.path.exists(datasets_dir):
        raise f"The directory does not exist -> {datasets_dir}"

    datasets = {}
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
            dataset = {"dataset_dir": current_dataset_path, "img_dir": img_path,
                       "annotations_dir": annotation_path}

            datasets[dataset_name] = dataset
            if not os.path.exists(annotation_path):
                raise f"No 'annotations' folder in {current_dataset_path}"

    return datasets


def generate_dataset_info(dataset_name, img_dir):
    """ Load the provided dataset and collect metadata """

    # collect all datasets metadata
    dataset_size = len(os.listdir(img_dir))
    dataset_type = os.path.splitext(os.listdir(img_dir)[0])[1]
    dataset = Dataset()
    dataset.record_dataseet_metadata(dataset_name, dataset_size, dataset_type)
    return dataset

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

    return models_data


def generate_image_info(dataset_dir, model_id):
    """ Load image and annotation files from directory and collect meta"""

    images_data = []

    # compute all image names
    img_dir = os.path.join(dataset_dir, "images")
    images_for_dataset = os.listdir(img_dir)

    dataset_name = os.path.dirname(dataset_dir)
    # compute all image and model_image metadata
    for img in images_for_dataset:
        img_meta = LoadImgMetadata(img, dataset_dir).load_all_metadata()
        img_model_meta = LoadImgModelData(img, dataset_dir, model_id).get_all_model_data()
        image = Image()

        image.record_img_metadata(img_meta["name"], img_meta["image_bbox"], img_meta["image_category"], dataset_name, model_id)
        image.record_model_img_metadata(img_model_meta["bbox"], img_model_meta["category_id"],
                                        img_model_meta["heatmap"], img_model_meta["activations"])
        images_data.append(image)

    return images_data


def add_data_to_db(db_dir, datasets_dir):
    # Open a connection with the database
    connection = sqlite3.connect(db_dir, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    datasets_paths = get_dataset_paths(datasets_dir)

    # Check if datasets names already exist and record them into the db
    for dataset_name in datasets_paths.keys():
        if Writer.check_dataset_name(dataset_name, cursor):
            raise Exception(f"A record with name {dataset_name} already exists in table routing_table")

    # generate dataset info
    datasets_info = []
    for dataset in datasets_paths.items():
        dataset_info = generate_dataset_info(dataset[0], dataset[1]['img_dir'])
        datasets_info.append(dataset_info)

    # Update Datasets table with the respective data
    for record in datasets_info:
        dataset_info = record.data()
        name = dataset_info['name']
        size = dataset_info['size']
        type = dataset_info['type']
        Writer.create_datasets_table_record(name, size, type, cursor)

    # Generate model info
    models_info = generate_model_info()
    # Update Models table with the respective data
    models = models_info
    for model in models:
        model_name = model.data()['name']
        model_id = model.data()['id']
        model_datasets = ",".join(model.data()['datasets'])
        Writer.create_models_table_record(model_name, model_id, model_datasets, cursor)

    # Generate img info and save into the DB
    for product in itertools.product(datasets_info, models_info):
        # Generating
        dataset_name = product[0].data()['name']
        dataset_dir = datasets_paths[dataset_name]['dataset_dir']
        model_id = product[1].data()['id']
        model_name = product[1].data()['name']
        model_name = model_name.lower()
        model_name = model_name.replace(' ', '_')
        images = generate_image_info(dataset_dir, model_id)
        # Write into the DB
        table_name = f"{dataset_name}_{model_name}"
        Writer.create_images_table(table_name, cursor)
        Writer.write_data_into_images_table(table_name, images, model_id, model_name, dataset_name, cursor)

    connection.commit()