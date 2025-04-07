# project_tree.py

import os

def print_directory_tree(start_path, prefix=""):
    files = os.listdir(start_path)
    files.sort()
    for index, file in enumerate(files):
        path = os.path.join(start_path, file)
        is_last = index == len(files) - 1
        connector = "└── " if is_last else "├── "
        print(prefix + connector + file)
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_directory_tree(path, prefix + extension)

if __name__ == "__main__":
    print("📁 프로젝트 디렉토리 구조")
    print_directory_tree(".")