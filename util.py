#!/usr/bin/env python3

#
# util.py
#
# Various utilities
#

from datetime import datetime
import os
import re

class Util:
    """
    Utility functions
    """
    DATA_DIR = "data"
    RESULTS_DIR = DATA_DIR + "/results"

    @staticmethod
    def read_list(filename: str) -> list:
        data_list = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding="ascii") as file:
                    data = file.read()
            except UnicodeDecodeError:
                with open(filename, 'r', encoding="utf-8") as file:
                    data = file.read()
            for line in data.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    data_list.append(line)
        return data_list
    
    @classmethod
    def save(cls, name: str, page, extension: str='') -> str:

        if not os.path.isdir(cls.RESULTS_DIR):
            os.makedirs(cls.RESULTS_DIR)

        now = datetime.now().strftime("%Y%m%d%H%M%S")

        filename = cls.RESULTS_DIR + "/" + re.sub(r"[ :\/]", "_", name) + "." + now
        filename = filename.replace("https___","")
        if extension:
            filename = f'{filename}.{extension}'

        if isinstance(page, bytes):
            handle  = open(filename, "wb")
            handle.write(page)
            handle.close()
        else:
            handle  = open(filename, "w", encoding="utf-8")
            handle.write(page)
            handle.close()

        print(f'Saved payload to {filename}')
        return filename
