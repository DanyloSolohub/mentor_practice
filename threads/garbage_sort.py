import os
from pathlib import Path

extensions = []


def create_folder(folder: Path):
    if not folder.exists():
        Path.mkdir(folder)


def replace_file(file_path: Path, new_path: Path):
    if file_path.exists():
        file_path.replace(new_path)


def delete_empty_directories(main_directory_path: Path):
    for element in main_directory_path.iterdir():
        if element.is_dir():
            delete_empty_directories(element)
            if not os.listdir(element):
                os.rmdir(element)


def clear_directory(path_to_sort: Path, result_path: Path):
    for element in path_to_sort.iterdir():
        if element.is_dir():
            clear_directory(element)
        elif element.is_file():
            suffix = element.suffix
            suffix_folder = result_path.joinpath(suffix)
            if suffix not in extensions:
                extensions.append(suffix)
                create_folder(suffix_folder)
            replace_file(element, suffix_folder.joinpath(element.name))


def main():
    path_to_sort = Path('/home/danylo/PycharmProjects/mentor_practice/GARBAGE')
    result_path = Path('/home/danylo/PycharmProjects/mentor_practice/SORTED')
    clear_directory(path_to_sort, result_path)
    print('Garbage is sorted')
    delete_empty_directories(path_to_sort)
    print('Empty directories are removed')


if __name__ == '__main__':
    exit(main())
