import os
import random
import shutil
import string
from typing import Union

import numpy as np
from PIL import Image


def __get_file_name(length: int = 10, ext: str = 'jpg') -> str:
    """
    Generates random file name.
    :param length: Length of char in filename.
    :param ext: Extension for file.
    :return: Generated filename.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) + f'.{ext}'


def __creatre_and_save_image(directory: str, height: int, width: int, name_length: int, file_ext: str) -> str:
    """
    Creates image and saves it.
    :param directory: Directory where image has to be saved.
    :param height: Height of image.
    :param width: Width of image.
    :param name_length: Length of char in filename.
    :param file_ext: filename extension.
    :return: Path to created image.
    """
    random_pix = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(random_pix)
    filename = os.path.abspath(os.path.join(directory, __get_file_name(name_length, file_ext)))
    img.save(filename)
    return filename


def _make_dir(directory: str) -> None:
    """
    Creates directory. If directory already exists it will be removed before creating it.
    :param directory:
    :return:
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def _prepare_images(directory: str,
                    img_num: int = 0,
                    fake_img_num: int = 0,
                    fake_ext_img_num: int = 0,
                    other_files_num: int = 0,
                    img_ext: str = 'jpg',
                    fake_img_ext: str = 'doc',
                    shape: Union[tuple, list] = (800, 600)) -> list:
    """
    Creates images in test directory.
    :param directory: Directory where images have to be saved.
    :param img_num: Number of valid images.
    :param fake_img_num: Number of files with image extension but no real images.
    :param fake_ext_img_num: Number valid images but with extension other than images.
    :param other_files_num: Number of other non-image files to create.
    :param img_ext: Extension of images to create.
    :param fake_img_ext: Extension of images with fake extension and other files.
    :param shape: Shape of images in format (width, height) or ((width, height), ...). Second format needs to have
    length equal to img_num + fake_ext_img_num.
    :return: List with images paths.
    """
    if len(shape) == 2:
        shape = [shape for _ in range(img_num + fake_ext_img_num)]
    images = []
    _make_dir(directory)
    for num in range(img_num):  # Real images with valid extension
        width, height = shape[num]
        images.append(__creatre_and_save_image(directory, height, width, 10, img_ext))
    for num in range(fake_img_num):  # Fake images
        with open(os.path.join(directory, __get_file_name(10, img_ext)), 'wb') as f:
            f.write(np.random.randint(0, 256, random.randint(100, 12400), dtype=np.uint8).tobytes())
    for num in range(fake_ext_img_num):  # Real images with fake extension
        width, height = shape[img_num + num]
        filename = __creatre_and_save_image(directory, height, width, 10, img_ext)
        new_ext_filename = os.path.join(os.path.dirname(filename),
                                        os.path.splitext(os.path.basename(filename))[0] + f'.{fake_img_ext}')
        os.rename(filename, new_ext_filename)
        images.append(new_ext_filename)
    for num in range(other_files_num):  # Other files
        with open(os.path.join(directory, __get_file_name(10, fake_img_ext)), 'wb') as f:
            f.write(np.random.randint(0, 256, random.randint(100, 12400), dtype=np.uint8).tobytes())
    return images


def _remove_test_dir(directory) -> None:
    """
    Removes test temporary directory.
    :return: None
    """
    try:
        shutil.rmtree(os.path.abspath(directory))
    except FileNotFoundError:
        print(f'[_remove_test_dir]: File {directory} not found.')
