"""operator json
@author: cjing9017
@date: 2020/04/02
"""
import json


class Json2Dict:

    @staticmethod
    def write_dict_to_json(dict_to_write, filename):
        json_str = json.dumps(dict_to_write)
        with open(filename, "w") as f:
            json.dump(json_str, f)

    @staticmethod
    def read_json_to_dict(filename):
        with open(filename, "r") as f:
            json_str = json.load(f)
            dict_to_read = json.loads(json_str)

        return dict_to_read
