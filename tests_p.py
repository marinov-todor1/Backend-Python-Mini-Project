import os
import numpy
import pytest
import cv2

from Load import LoadImgMetadata
import Processor

dataset_dir = "dataset_data/human_dataset/"
dataset_img_dir = "dataset_data/human_dataset/images"


#test if the provided bbox coordinates are within the image size
def test_bbox_coordinates():
    """ Test if the provided bbox coordinates are within the image size """
    input_sample_name = os.listdir(dataset_img_dir)[0]
    input_sample_path = os.path.join(dataset_img_dir, input_sample_name)
    test_input = cv2.imread(input_sample_path, cv2.IMREAD_UNCHANGED)
    input_size = test_input.shape
    input_sample_bbox = LoadImgMetadata(input_sample_name, dataset_dir).load_img_bbox()

    for bbox in input_sample_bbox:
        bbox_height = bbox[3]
        bbox_width = bbox[2]
        assert input_size[0] >= bbox_height and input_size[1] >= bbox_width


def test_img_type():
    """ Test if all images in a folder are the same type """
    img_list = os.listdir(dataset_img_dir)
    base_extension = os.path.splitext(img_list[0])[1]
    for img in img_list[1:]:
        img_extension = os.path.splitext(img)[1]
        assert img_extension == base_extension


def test_num_processed_objects():
    """ Test if all images were processed """
    model_id = 0
    dataset_size = len(os.listdir(dataset_img_dir))
    count_of_processed_images = len(Processor.generate_image_info(dataset_dir, model_id))
    assert dataset_size == count_of_processed_images


def test_if_category_in_range():
    """ Test if the provided category_ids are withing range """
    input_sample_name = os.listdir(dataset_img_dir)[0]
    annotations_folder = os.path.join(dataset_dir, "annotations")

    category_id = LoadImgMetadata(input_sample_name, dataset_dir).load_img_category()
    for category in category_id:
        assert category in range(0, 4)


def test_load_img_bbox():
    """ Test the load_img_bbox function for expected output """
    test_bbox = LoadImgMetadata("11.jpg", "./dataset_data/human_dataset/").load_img_bbox()
    expected_result = [[14, 0, 29, 17], [28, 34, 43, 39], [21, 31, 39, 38]]
    assert numpy.array_equal(test_bbox, expected_result)


def test_load_img_category():
    """ Test the load_img_category function for expected output """
    test_category = LoadImgMetadata("11.jpg", "./dataset_data/human_dataset/").load_img_category()
    expected_result = [1, 2, 0]
    assert numpy.array_equal(test_category, expected_result)


def test_get_dataset_paths():
    """ Test the get_dataset_paths function for expected output"""
    test_result = Processor.get_dataset_paths("./dataset_data/human_dataset/")
    expected_result = {'human_dataset': {'dataset_dir': '/Users/todo/PycharmProjects/Tenyks/dataset_data/human_dataset',
                        'img_dir': '/Users/todo/PycharmProjects/Tenyks/dataset_data/human_dataset/images',
                        'annotations_dir': '/Users/todo/PycharmProjects/Tenyks/dataset_data/human_dataset/annotations'}}

    assert numpy.array_equal(test_result, expected_result)


def test_generate_dataset_info():
    """ Test the generate_dataset_info function for expected output"""
    test_result = Processor.generate_dataset_info("human_dataset",
                                                  "/Users/todo/PycharmProjects/Tenyks/dataset_data/human_dataset/images/")

    assert test_result.data() == {'name': 'human_dataset', 'size': 12, 'type': '.jpg'}


def test_generate_model_info():
    """ Test the generate_model_info function for expected output"""
    test_result = Processor.generate_model_info()
    assert test_result[0].data() == {'name': 'Hybrid Model', 'id': 0, 'datasets': ['human_dataset', 'terminator_dataset']}


def test_generate_image_info():
    """ Test the generate_image_info function for expected output (partially, as models are randomly generated) """
    test_result = Processor.generate_image_info("./dataset_data/human_dataset/", 0)
    test_result = test_result[0].data()
    test_result = {'name': test_result['name'], 'img_bbox': test_result['img_bbox'], 'img_category': test_result['img_category']}
    expected = {'name': '14.jpg', 'img_bbox': [[23, 11, 34, 20], [34, 35, 51, 52], [30, 6, 49, 11]], 'img_category': [2, 1, 1]}
    assert test_result == expected


def main():
    test_get_dataset_paths()


if __name__ == "__main__":
    main()