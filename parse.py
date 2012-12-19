import sys
import os
import logging

class FileHandler:

    def __init__(self):
        self.f = None

    def set_file(self, filename):
        self.f = file(self.filename)
        logging.debug("%s is set" % (filename))

    def close_file(self):
        self.f.close()


class DTDParser:

    def __init__(self):
        self.dict = dict()
        self.file_handler = FileHandler()

    def parse(self, filename):
        self.file_handler.set_file(filename)
        for line in self.file_handler.f.readlines():
            if line.startswith("<!ENTITY"):
                line_info = line.split() #<!ENTITY robots.errorTitleText "Welcome Humans!">
                if len(line_info) == 3:
                    key = line_info[1]
                    value = True # not interested the value itself, just the existence
                    self.dict[key] = value
        self.file_handler.close()
        return self.dict

class PropertiesParser:

    def __init__(self):
        self.dict = dict()
        self.file_handler = FileHandler()

    def parse(self, filename):
        self.file_handler.set_file(filename)
        for line in self.file_handler.f.readlines():
            if line.startswith("#"):
                continue
            else:
                line_info = line.split("=") #<!ENTITY robots.errorTitleText "Welcome Humans!">
                if len(line_info) == 2:
                    key = line_info[0]
                    value = True # not interested the value itself, just the existence
                    self.dict[key] = value
        self.file_handler.close()
        return self.dict

if __name__ == "__main__":

    dtd_parser = DTDParser()
    dtd_file_dict1 = dict()
    dtd_file_dict2 = dict()

    properties_parser = PropertiesParser()
    properties_file_dict1 = dict()
    properties_file_dict2 = dict()

    path1 = sys.argv[1]
    path2 = sys.argv[2]

    for root, dirs, files in os.walk(path1):
        if os.path.isfile(root):
            if root.endswith(".dtd"):
                dtd_file_dict1[root] = dtd_parser.parse(root)
            if root.endswith(".properties"):
                properties_file_dict1[root] = properties_parser.parse(root)

    for root, dirs, files in os.walk(path2):
        if os.path.isfile(root):
            if root.endswith(".dtd"):
                dtd_file_dict2[root] = dtd_parser.parse(root)
            if root.endswith(".properties"):
                properties_file_dict2[root] = properties_parser.parse(root)


    # here is the comparison
    dtd_keys1 = dtd_file_dict1.keys()
    dtd_keys2 = dtd_file_dict2.keys()

    for key in dtd_keys1:
        if key in dtd_keys2:
            dtd_value1 = dtd_file_dict1[key]
            dtd_value2 = dtd_file_dict2[key]

            value_diff = set(dtd_value1) - set(dtd_value2)

            if len(value_diff) > 0:
                logging.debug("\t %s" % (key))
                value_li = list(value_diff)
                for value in value_li:
                    logging.debug("\t %s" % (value))

    properties_keys1 = properties_file_dict1.keys()
    properties_keys2 = properties_file_dict2.keys()

    for key in properties_keys1:
        if key in properties_keys2:
            properties_value1 = properties_file_dict1[key]
            properties_value2 = properties_file_dict2[key]

            value_diff = set(properties_value1) - set(properties_value2)

            if len(value_diff) > 0:
                logging.debug("\t %s" % (key))
                value_li = list(value_diff)
                for value in value_li:
                    logging.debug("\t %s" % (value))
