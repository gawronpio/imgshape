import os
import sys

import pytest

sys.path.append(os.path.abspath('./'))
from tests import _remove_test_dir

from imgshape.imgshape import _save_csv


class Test:
    __test_dir = 'test_tmp'

    @staticmethod
    def _prepare_dir() -> None:
        """
        Creates test temporary directory
        :return: None
        """
        if os.path.exists(Test.__test_dir):
            _remove_test_dir(Test.__test_dir)
        os.mkdir(Test.__test_dir)

    def test_save_csv_valid_path_and_data(self):
        """
        Tests that the function saves data to a CSV file with a valid path and valid data.
        """
        # Given
        path = os.path.join(Test.__test_dir, 'valid_path.csv')
        data = {'key1': 'val1', 'key2': 'val2'}
        Test._prepare_dir()

        # When
        _save_csv(path, data)

        # Then
        assert os.path.exists(path)
        with open(path, 'r') as fr:
            content = fr.read()
            assert content == 'key1,val1\nkey2,val2\n'

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_save_csv_empty_data(self):
        """
        Tests that the function don't save empty data to a CSV file.
        """
        # Given
        path = os.path.join(Test.__test_dir, 'valid_path.csv')
        data = {}
        Test._prepare_dir()

        # When
        _save_csv(path, data)

        # Then
        assert not os.path.exists(path)

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_save_csv_invalid_path(self):
        """
        Tests that the function raises an exception when saving data to a CSV file with an invalid path.
        """
        # Given
        path = Test.__test_dir + '/\\/invalid_path.csv'
        data = {'key1': 'val1', 'key2': 'val2'}

        # When, Then
        with pytest.raises(Exception):
            _save_csv(path, data)

    def test_save_csv_special_characters(self):
        """
        Tests that the function saves data with special characters to a CSV file with a valid path.
        """
        # Given
        path = os.path.join(Test.__test_dir, 'valid_path.csv')
        data = {'key1': 'val1a, val1b', 'key2, key': 'val2'}
        Test._prepare_dir()

        # When
        _save_csv(path, data)

        # Then
        assert os.path.exists(path)
        with open(path, 'r') as fr:
            content = fr.read()
            assert content == 'key1,"val1a, val1b"\n"key2, key",val2\n'

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_save_csv_large_data(self):
        """
        Tests that the function saves large data to a CSV file with a valid path.
        """
        # Given
        path = os.path.join(Test.__test_dir, 'valid_path.csv')
        data = {'key' + str(i): 'val' + str(i) for i in range(10000)}
        Test._prepare_dir()

        # When
        _save_csv(path, data)

        # Then
        assert os.path.exists(path)
        with open(path, 'r') as fr:
            content = fr.read()
            expected_content = '\n'.join([f'key{i},val{i}' for i in range(10000)]) + '\n'
            assert content == expected_content

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_save_csv_other_types(self):
        """
        Test that the function saves other types than string.
        """
        # Given
        path = os.path.join(Test.__test_dir, 'valid_path.csv')
        data = {(100, 200): 'val1', 'key2': [183, ], (100,): 'val3'}
        Test._prepare_dir()

        # When
        _save_csv(path, data)

        # Then
        assert os.path.exists(path)
        with open(path, 'r') as fr:
            content = fr.read()
            assert content == '"(100, 200)",val1\nkey2,[183]\n"(100,)",val3\n'

        # Post actions
        _remove_test_dir(Test.__test_dir)
