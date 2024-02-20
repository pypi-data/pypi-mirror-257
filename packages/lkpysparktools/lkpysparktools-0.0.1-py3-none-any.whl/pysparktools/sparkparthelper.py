from pysparktools import LogHelper
import re
from collections import OrderedDict
import functools as ft


class SparkPartHelper(LogHelper):
    
    @classmethod
    def get_part_name_value_list_from_path(cls, path):
        valid_pattern = "([^/]+)"
        part_pattern = f"({valid_pattern}={valid_pattern})"
        matches = re.findall(part_pattern, path)
        return matches
    
    @classmethod
    def get_part_name_value_dict_from_path(cls, path):
        part_name_value_list = cls.get_part_name_value_list_from_path(path)
        part_name_value_dict = OrderedDict({nv[1]:nv[2] for nv in part_name_value_list})
        return part_name_value_dict
    
    @classmethod
    def get_part_value_from_path_part_name(cls, path, part_name = '(?s:.*)'):
        group1 = f"({part_name})"
        group2 = "([^/]+)"
        pattern = f"{group1}={group2}"
        match = re.search(pattern, path)
        return match.group(2) if (match) else None
    
    @classmethod
    def get_basepath_from_path(cls, path):
        valid_pattern = "([a-z|A-Z|0-9|-|_]*)"
        basepath_pattern = "([a-z|A-Z|0-9|-|_|/|:]+)"
        part_pattern = f"({valid_pattern}={valid_pattern})"
        pattern = f"{basepath_pattern}/{part_pattern}"
        match = re.search(pattern, path)

        if match:
            basepath = match.group(1)
        else:
            basepath = path

        return basepath
    
    @classmethod
    def get_name_value_path_from_path(cls, path):
        lst = cls.get_part_name_value_list_from_path(path)
        name_value_path = ft.reduce(lambda t1, t2 : (t1[0] + '/' + t2[0],), lst)[0]
        return name_value_path