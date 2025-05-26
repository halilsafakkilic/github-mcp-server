import os


def get_root_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.dirname(current_dir)


ROOT_DIR = get_root_dir()
