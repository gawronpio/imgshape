import os
import sys

sys.path.append(os.path.abspath('./'))
from tests import _prepare_images, _remove_test_dir

from imgshape.imgshape import _get_picture_list


class Test:
    __test_dir = 'test_tmp'

    def test_get_picture_list_with_directory_only_image_files_non_recursive(self):
        """
        Tests that the function collects all image files in a directory that contains only image files.
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir, img_num=5)

        # When
        result = _get_picture_list(Test.__test_dir, recursive=False)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_picture_list_with_directory_only_image_files_recursive(self):
        """
        Tests that the function collects all image files in a directory that contains only image files.
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir, img_num=5)

        # When
        result = _get_picture_list(Test.__test_dir, recursive=True)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_picture_list_with_directory_nested_image_files(self):
        """
        Tests that the function collects all image files in a directory that contains nested image files.
        :return:
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir, img_num=5)
        expected_images.extend(_prepare_images(os.path.join(Test.__test_dir, 'nested'), img_num=5))

        # When
        result = _get_picture_list(Test.__test_dir, recursive=True)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_picture_list_with_directory_nested_image_files_non_recursive(self):
        """
        Tests that the function collects all image files in a directory that contains nested image files but with disabled recursive mode.
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir, img_num=5)
        _prepare_images(os.path.join(Test.__test_dir, 'nested'), img_num=5)

        # When
        result = _get_picture_list(Test.__test_dir, recursive=False)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_picture_list_with_directory_image_and_non_image_files(self):
        """
        Tests that the function collects only image files in a directory that contains both image and non-image files.
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir, img_num=5, other_files_num=3)

        # When
        result = _get_picture_list(Test.__test_dir, recursive=True)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_picture_list_with_directory_image_non_image_and_image_with_fake_extension_files(self):
        """
        Tests that the function collects only image files in a directory that contains both image, non-image and
        images with fake extension files.
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir, img_num=5, fake_ext_img_num=3)

        # When
        result = _get_picture_list(Test.__test_dir, recursive=True)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_get_picture_list_with_full_spectrum_of_options(self):
        """
        Tests that the function collects only image files in a directory that contains different type of files and
        nested directory
        """
        # Given
        expected_images = _prepare_images(Test.__test_dir,
                                          img_num=6,
                                          fake_ext_img_num=5,
                                          fake_img_num=4,
                                          other_files_num=3)
        expected_images.extend(_prepare_images(os.path.join(Test.__test_dir, 'nested1'),
                                               img_num=6,
                                               fake_ext_img_num=5,
                                               fake_img_num=4,
                                               other_files_num=3))
        expected_images.extend(_prepare_images(os.path.join(Test.__test_dir, 'nested2'),
                                               img_num=6,
                                               fake_ext_img_num=5,
                                               fake_img_num=4,
                                               other_files_num=3))

        # When
        result = _get_picture_list(Test.__test_dir, recursive=True)

        # Then
        assert sorted(result) == sorted(expected_images)

        # Post actions
        _remove_test_dir(Test.__test_dir)
