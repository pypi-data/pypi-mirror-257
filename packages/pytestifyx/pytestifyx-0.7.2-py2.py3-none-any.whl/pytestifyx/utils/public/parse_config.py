import os
import configparser

from pytestifyx.utils.public.get_project_path import get_project_path


def parse_config(file_path):
    config = configparser.ConfigParser()
    base_path = get_project_path()
    full_path = os.path.join(str(base_path), file_path)
    config.read(full_path, encoding='utf-8')
    return config
