# TODO
# Interface for writing in the DB (probably singleton if the DB does not have auto-lock functionality)
import sqlite3

db_dir = "./datasets.db"


# check if training dataset already exist with such name
def check_dataset_name(dataset_name, cursor):
    """ Validates if record with name X already exists in training_datasets table """
    query = "SELECT EXISTS(SELECT * FROM routing_table WHERE dataset_name = ?)"
    parameters = (dataset_name,)
    cursor.execute(query, parameters)
    records = cursor.fetchall()
    return records[0][0]


def create_routing_table_record(dataset_name, cursor):
    """ Create new routing_table record """
    query = "INSERT OR IGNORE INTO routing_table (dataset_name) VALUES (?)"
    parameters = (dataset_name,)
    cursor.execute(query, parameters)


def create_models_table_record(model_name, model_id, training_datasets, cursor):
    query = "INSERT OR IGNORE INTO models (name, training_datasets, model_id) VALUES (?, ?, ?)"
    parameters = (model_name, training_datasets, model_id)
    cursor.execute(query, parameters)


def create_datasets_table_record(name, size, type, cursor):
    query = "INSERT OR IGNORE INTO datasets(name, size, type) VALUES (?, ?, ?)"
    parameters = (name, size, type)
    cursor.execute(query, parameters)


def create_images_table(dataset_name, cursor):
    query = "CREATE TABLE ?(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, bbox"
    # Only creates the table and return it's name
    pass


def write_data_into_images_table(table_name, img_info, cursor):
    # Create image records one by one
    # Add models(model_id) foreign key
    # Add datasets(name) foreign key
    pass
