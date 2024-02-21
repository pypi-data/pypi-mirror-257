# -*- coding: utf-8 -*-
"""
Set directory of applicaciton to store data.
"""

import sys
import os


def get_platform() -> str:
    """
    Gets the directory path to store data depending on the platform.
    Creates the directory if it does not exist.

    Returns:
        str: path for store data.
    """
    dir_path = None
    DIR_ROOT = 'filesignaturecollectors'
    HOME_DIR = os.path.expanduser('~')

    platform = sys.platform

    if platform == 'linux':
        dir_path = os.path.join(HOME_DIR, '.config', DIR_ROOT)
    elif platform == 'win32':
        dir_path = os.path.join(os.getenv('APPDATA'), DIR_ROOT)
    elif platform == 'darwin':
        dir_path = os.path.join(
                                HOME_DIR,
                                '/Library/Application Support',
                                DIR_ROOT
                            )

    abs_path = os.path.abspath(dir_path)

    print(abs_path)

    if not os.path.exists(abs_path):
        os.makedirs(abs_path)

    return abs_path
