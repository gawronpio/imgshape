import argparse
import csv
import os
import sys
from typing import Dict, Optional, Tuple

import filetype
from matplotlib import pyplot as plt
from PIL import Image

from imgshape.version import __version__


def _read_csv(path: str) -> Optional[dict]:
    """
    Reads csv file and returns content as a dict.
    :param path: Path to file to read.
    :return: Content of the file as a dict, or None if there was an error.
    """
    try:
        with open(path, 'r') as f:
            data = {}
            for line in csv.reader(f):
                if len(line) == 0:
                    continue
                if len(line) == 1:
                    data[line[0]] = ''
                elif len(line) == 2:
                    data[line[0]] = line[1]
                else:
                    data[line[0]] = ''.join(line[1:])
            return data
    except FileNotFoundError:
        return None


def _save_csv(path: str,
              data: dict) -> None:
    """
    Saves data to CSV file.
    :param path: Path to the file for saving data.
    :param data: Data to save.
    :return: None
    """
    if data:
        with open(path, 'w') as fw:
            for key, value in data.items():
                key = str(key)
                if ',' in key:
                    key = f'"{key}"'
                value = str(value)
                if ',' in value:
                    value = f'"{value}"'
                fw.write(f'{key},{value}\n')


def _get_picture_list(directory: str, recursive: bool = False, follow_symlinks: bool = True) -> list:
    """
    Collects image files in a directory. If recursive is True images are collected in nested directories.
    :param directory: Directory in which to search for images.
    :param recursive: If True, searches for images in nested directories.
    :param follow_symlinks: If True, the search for images will follow directories pointed to by symlinks only if recursive is set to True.
    :return: List of absolute paths to image files.
    """
    if recursive:
        files = []
        for root, _, fs in os.walk(directory, followlinks=follow_symlinks):
            for file in fs:
                file = os.path.abspath(os.path.join(root, file))
                if os.path.isfile(file):
                    files.append(file)
    else:
        files = [os.path.abspath(entry.path) for entry in os.scandir(directory) if entry.is_file()]
    images = [file for file in files if filetype.guess(file) is not None and filetype.guess(file).mime.split('/')[0] == 'image']
    return images


def _get_shapes(directory: Optional[str] = None,
                recursive: bool = False,
                follow_symlinks: bool = True,
                read_file: Optional[str] = None) -> Dict[Tuple[int, int], int]:
    """
    Reads files and prepares images shapes dictionary.
    :param directory: Input directory to search images.
    :param recursive: True if images must be searched in subdirectories.
    :param follow_symlinks: True if images must be searched in directories pointed to by symbolic links.
    :param read_file: Path to file with saved list of shapes tp read instead of checking images.
    :return:None
    """
    shapes = dict()
    if read_file is not None:  # Read shapes from file
        _shapes = _read_csv(read_file)
        shapes = {}
        if _shapes is None:
            raise ValueError(f'Input file "{read_file}" does not exist or corrupted.')
        for shape_key in _shapes:
            if not isinstance(shape_key, str):
                raise ValueError(f'Input file "{read_file}" corrupted.')
            key = tuple(map(int, shape_key.strip('() ').split(',')))
            val = int(_shapes[shape_key])
            shapes[key] = val
    elif directory is not None:  # Search for images and read shapes
        images = _get_picture_list(directory=directory, recursive=recursive, follow_symlinks=follow_symlinks)
        if len(images) == 0:
            raise ValueError(f'Input directory "{directory}" does not contain any images.')
    else:
        raise ValueError('Either input file or directory must be specified.')

    if not shapes.keys():
        for image in images:
            try:
                img = Image.open(image)
            except Exception:  # pylint: disable=broad-except
                continue
            s = img.size
            if s in shapes:
                shapes[s] += 1
            else:
                shapes[s] = 1

    return shapes


def plot_shapes(shapes: dict) -> None:
    """
    Plots images shapes distribution.
    :param shapes: Dictionary with image shapes.
    :return: None
    """
    res, count = zip(*list(sorted(shapes.items(), key=lambda x: x[1])))
    if len(res) > 1:
        min_diameter = 1
        max_diameter = int((max(max(res)) - min(min(res))) * 0.1)
        a = (max_diameter - min_diameter) / (max(count) - min(count))
        b = min_diameter - a * min(count)
        diameters = [c * a + b for c in count]
    else:
        diameters = [50]
    points = plt.scatter(*zip(*res), s=diameters, alpha=0.5, c='deepskyblue', edgecolors='mediumblue')

    def on_hover(event):
        if event.inaxes == plt.gca():
            contains, ind = points.contains(event)
            if contains:
                r = res[ind["ind"][0]]
                c = count[ind["ind"][0]]
                p = plt.gca()
                title = '\n'.join(p.get_title().split('\n')[:-1])
                title += f'\nResolution: ({r[0]}x{r[1]}), Images count: {c}'
                p.set_title(title)
                plt.show()
            else:
                p = plt.gca()
                p.set_title('\n'.join(p.get_title().split('\n')[:-1]) + '\n')

    plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

    plt.title('Distribution of the number of images in relation to resolution.\n'
              f'Max count res: {res[count.index(max(count))]}\n')
    plt.xlabel('Horizontal resolution')
    plt.ylabel('Vertical resolution')
    plt.show()


def read_shapes(directory: str,
                recursive: bool = False,
                follow_symlinks: bool = True,
                read_file: Optional[str] = None,
                save_file: Optional[str] = None) -> None:
    """
    Reads shapes of images and displays their distribution and minimum and maximum values.
    :param directory: Input directory to search images.
    :param recursive: True if images must be searched in subdirectories.
    :param follow_symlinks: True if images must be searched in directories pointed to by symbolic links.
    :param read_file: Path to file with saved list of shapes tp read instead of checking images.
    :param save_file: Path to file to save list of shapes.
    :return:None
    """
    shapes = _get_shapes(directory=directory, recursive=recursive, follow_symlinks=follow_symlinks, read_file=read_file)
    if save_file is not None:
        _save_csv(save_file, shapes)
    plot_shapes(shapes)


def main() -> None:
    """
    Main function.
    :return: None
    """
    parser = argparse.ArgumentParser(prog='imgshape',
                                     description='The program checks the shape of images and shows them distribution '
                                                 'and minimum and maximum values.')
    parser.add_argument('-i', '--inputdir',
                        help='Input directory with images to check the shape of the images.',
                        action='store')
    parser.add_argument('-R', '--recursive',
                        help='Check images in all subdirectories.',
                        action='store_true')
    parser.add_argument('-S', '--followsymlinks',
                        help='Follow directories pointed to by symbolic links when searching for images.',
                        action='store_true')
    parser.add_argument('-r', '--read',
                        help='Reads list of shapes from file instead of checking images.',
                        action='store')
    parser.add_argument('-s', '--save',
                        help='Saves list of shapes to CSV file',
                        action='store')
    parser.add_argument('-V', '--version', help='Program version', action='store_true')
    args = parser.parse_args()

    if args.version:
        print(f'c2bw version: {__version__}')
        sys.exit(0)

    if args.read is None:
        if args.inputdir is None or not os.path.exists(args.inputdir):
            print(f'Input directory "{args.inputdir}" does not exist.')
            sys.exit(1)
        if not os.path.isdir(args.inputdir):
            print(f'Input directory "{args.inputdir}" is not a directory.')
            sys.exit(1)
        if not os.path.isabs(args.inputdir):
            args.inputdir = os.path.abspath(args.inputdir)
    else:
        if not os.path.exists(args.read):
            print(f'Input file "{args.read}" does not exist.')
            sys.exit(1)
        if not os.path.isfile(args.read):
            print(f'Input file "{args.read}" is not a file.')
            sys.exit(1)
        if not os.path.isabs(args.read):
            args.read = os.path.abspath(args.read)

    # Check save file
    if args.save is not None:
        if os.path.exists(args.save):
            print(f'Output file "{args.save}" already exist.')
            sys.exit(1)
        if not os.path.isabs(args.save):
            args.save = os.path.abspath(args.save)

    try:
        read_shapes(directory=args.inputdir,
                    recursive=args.recursive,
                    follow_symlinks=args.followsymlinks,
                    read_file=args.read,
                    save_file=args.save)
    except Exception as e:  # pylint: disable=broad-except
        print('#' * 50)
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
