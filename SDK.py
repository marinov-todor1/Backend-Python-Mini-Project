import Processor
import Reader
import sqlite3

db_dir = "./datasets.db"

connection = sqlite3.connect(db_dir, detect_types=sqlite3.PARSE_DECLTYPES)
cursor = connection.cursor()


def main():
    # From user: get path to folder containing datasets for processing
    datasets_dir = input("Enter the path to the parent folder (containing subfolders with datasets) for processing.\n"
                         "Example: /Users/todo/PycharmProjects/Tenyks/dataset_data\n")

    # SDK sample call to extract and save all data into the DB
    try:
        Processor.add_data_to_db(db_dir, datasets_dir)
    # In Processor.py (line 111) there is a check preventing the user from inserting two datasets with the same name in
    # the DB. Hence, running the SDK.py a second time will raise an error. The purpose of this try-except is strickly
    # for review purposes.
    # Also the DB is protected with CREATE TABLE IF NOT EXISTS
    except:
        pass

    # SDK sample call to load single image data
    image = Reader.read_img_data("human_dataset", "hybrid_model", "111.jpg", cursor)
    image_name = image.data()['name']
    image_bbox = image.data()['img_bbox']
    image_category = image.data()['img_category']
    image_model_bbox = image.data()['model_image_bbox']
    image_model_category = image.data()['model_image_category']
    image_model_heatmap = image.data()['model_image_heatmap']  # retrieved as strings -> NOT OK
    image_model_activations = image.data()['model_image_activations']  # retrieved as strings -> NOT OK

    # print all data in bulk
    print(image.data())
    print("-----------------------------------------------")

    # SDK sample call to load model data
    model = Reader.read_model_data("Hybrid Model", cursor)
    print(model.data())
    print("-----------------------------------------------")

    # SDK sample call to load dataset data
    dataset = Reader.read_dataset_data("human_dataset", cursor)
    print(dataset.data())
    print("-----------------------------------------------")


if __name__ == "__main__":
    main()
