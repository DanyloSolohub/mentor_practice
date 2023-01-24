import os
from pathlib import Path
from threading import Thread

extensions = []
threads: list[Thread] = []


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


def create_extension_folder(suffix: str, path: Path) -> Path:
    suffix_folder = path.joinpath(suffix)
    if suffix not in extensions:
        extensions.append(suffix)
        create_folder(suffix_folder)
    return suffix_folder


def clear_directory(path_to_sort: Path, result_path: Path):
    for element in path_to_sort.iterdir():
        if element.is_dir():
            folder_thread = Thread(
                target=clear_directory,
                args=(element, result_path),
                name=str(element)
            )
            folder_thread.start()
            threads.append(folder_thread)
        elif element.is_file():
            suffix_folder = create_extension_folder(element.suffix, result_path)
            file_thread = Thread(
                target=replace_file,
                args=(element, suffix_folder.joinpath(element.name)),
                name=str(element)
            )
            file_thread.start()
            threads.append(file_thread)


def main():
    path_to_sort = Path('/home/danylo/PycharmProjects/mentor_practice/GARBAGE')
    result_path = Path('/home/danylo/PycharmProjects/mentor_practice/SORTED')
    clear_directory(path_to_sort, result_path)
    for thread in threads:
        print(thread.name)
        thread.join()
    print('Garbage is sorted')
    delete_empty_directories(path_to_sort)
    print('Empty directories are removed')


if __name__ == '__main__':
    exit(main())
