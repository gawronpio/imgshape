import os
import sys

import pytest

sys.path.append(os.path.abspath('./'))
from tests import _make_dir, _prepare_images, _remove_test_dir

from imgshape.imgshape import _get_shapes


class Test:
    __test_dir = 'test_tmp'

    @staticmethod
    def __prepare_shapes(shapes: list) -> dict:
        """
        Prepares shapes in dictionary form.
        :param shapes: Shapes in list.
        :return: Shapes in dictionary form.
        """
        dict_shapes = {}
        for shape in shapes:
            if shape in dict_shapes.keys():
                dict_shapes[shape] += 1
            else:
                dict_shapes[shape] = 1
        return dict_shapes

    def test_get_shapes_with_directory_containing_images_with_different_shapes(self):
        """
        Tests that the function correctly reads the shapes of images in a directory containing images with different shapes.
        """
        # Given
        img_shapes = [(100, 200),
                      (200, 100),
                      (800, 600),
                      (600, 800),
                      (1920, 1040),
                      (800, 600),
                      (100, 200)]
        expected_shapes = Test.__prepare_shapes(img_shapes)
        img_num = 4
        _prepare_images(Test.__test_dir, img_num=img_num, fake_ext_img_num=len(img_shapes) - img_num, shape=img_shapes)

        # When
        shapes = _get_shapes(Test.__test_dir, recursive=True, follow_symlinks=True, read_file=None)

        # Then
        assert shapes == expected_shapes

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_shapes_with_empty_directory(self):
        """
        Tests that the function raises a ValueError when given an empty directory.
        """
        # Given
        _make_dir(Test.__test_dir)

        # When/Then
        with pytest.raises(ValueError):
            _get_shapes(Test.__test_dir, recursive=True, follow_symlinks=True, read_file=None)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_shapes_with_non_existing_directory(self):
        """
        Tests that the function raises a ValueError when given a non-existing directory.
        """
        # Given
        _remove_test_dir(Test.__test_dir)

        # When/Then
        with pytest.raises(ValueError):
            _get_shapes(Test.__test_dir, recursive=True, follow_symlinks=True, read_file=None)

    def test_get_shapes_from_file(self):
        """
        Tests that the function correctly reads the shapes of images from a file.
        """
        # Given
        img_shapes = [(100, 200),
                      (200, 100),
                      (800, 600),
                      (600, 800),
                      (1920, 1040),
                      (800, 600),
                      (100, 200)]
        expected_shapes = Test.__prepare_shapes(img_shapes)
        _make_dir(Test.__test_dir)
        file_path = os.path.join(Test.__test_dir, 'test.csv')
        with open(file_path, 'w') as f:
            f.write('\n'.join([f'"{shape_k}",{shape_v}' for shape_k, shape_v in expected_shapes.items()]))

        # When
        shapes = _get_shapes(read_file=file_path)

        # Then
        assert shapes == expected_shapes

        # Post actions
        _remove_test_dir(Test.__test_dir)
