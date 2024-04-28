import os
import sys

sys.path.append(os.path.abspath('./'))
from tests import _remove_test_dir

from imgshape.imgshape import _read_csv


class Test:
    __test_dir = 'test_tmp'

    @staticmethod
    def _prepare_test_file(filename: str, data: str) -> str:
        """
        Creates test directory and file needed for further tests.
        :param filename: Filename to create for tests.
        :param data: Data to save in test file.
        :return: path to test file.
        """
        path = os.path.join(Test.__test_dir, filename)
        if os.path.exists(Test.__test_dir):
            _remove_test_dir(Test.__test_dir)
        os.mkdir(Test.__test_dir)
        with open(path, 'w') as f:
            f.write(data)
        return path

    def test_read_valid_csv_with_one_line(self):
        """
        Tests that the function can read a valid csv file with one line
        """
        # Given
        path = Test._prepare_test_file('valid_csv_one_line.csv', 'key1,val1')

        # When
        result = _read_csv(path)

        # Then
        assert result == {'key1': 'val1'}

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_read_valid_csv_with_multiple_lines(self):
        """
         Tests that the function can read a valid csv file with multiple lines
        """
        # Given
        path = Test._prepare_test_file('valid_csv_multiple_lines.csv',
                                       'key1,val1\nkey2,val2\nkey3,val3\n')

        # When
        result = _read_csv(path)

        # Then
        assert result == {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_read_valid_csv_with_empty_lines(self):
        """
        Tests that the function can read a valid csv file with empty lines
        """
        # Given
        path = Test._prepare_test_file('valid_csv_with_empty_lines.csv',
                                       'key1,val1\n\n\nkey2,val2\nkey3,val3\n')

        # When
        result = _read_csv(path)

        # Then
        assert result == {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_read_valid_csv_with_empty_values(self):
        """
        Tests that the function can read a valid csv file with empty values
        """
        # Given
        path = Test._prepare_test_file('valid_csv_with_empty_values.csv',
                                       'key1,\nkey2,\nkey3,\n')

        # When
        result = _read_csv(path)

        # Then
        assert result == {'key1': '', 'key2': '', 'key3': ''}

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_read_empty_csv_file(self):
        """
        Tests that the function returns empty dictionary when reading an empty csv file
        """
        # Given
        path = Test._prepare_test_file('empty_csv_file.csv', '')

        # When
        result = _read_csv(path)

        # Then
        assert isinstance(result, dict)
        assert not result

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_read_csv_file_with_missing_values(self):
        """
        Tests that the function can read a csv file with missing values
        """
        # Given
        path = Test._prepare_test_file('csv_file_with_missing_values.csv',
                                       'key1,val1\nkey2,\nkey3,val3\n')

        # When
        result = _read_csv(path)

        # Then
        assert result == {'key1': 'val1', 'key2': '', 'key3': 'val3'}

        # Post actions
        _remove_test_dir(Test.__test_dir)

    def test_read_csv_file_with_string_and_coma(self):
        """
        Test that the function can read a csv fiale with string (marked by "") containing coma
        """
        # Given
        path = Test._prepare_test_file('csv_file_with_string_and_coma.csv',
                                       '"key1, key",val1\nkey2,"val2, val"\nkey3,val3\n')

        # When
        result = _read_csv(path)

        # Then
        assert result == {'key1, key': 'val1', 'key2': 'val2, val', 'key3': 'val3'}

        # Post actions
        _remove_test_dir(Test.__test_dir)
