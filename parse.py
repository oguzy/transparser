import sys
import os
import log

class FileHandler:

    def __init__(self):
        self.f = None
        self.logger = log.Logger("file_handler")

    def set_file(self, filename):
        self.f = file(filename)
        self.logger.message("%s is set" % filename)

    def close(self):
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

    logger = log.Logger("trans_parse")

    dtd_parser = DTDParser()
    dtd_file_dict1 = dict()
    dtd_file_dict2 = dict()

    properties_parser = PropertiesParser()
    properties_file_dict1 = dict()
    properties_file_dict2 = dict()

    path1 = sys.argv[1]
    path2 = sys.argv[2]

    for root, dirs, files in os.walk(path1):
        for f in files:
            file_path = os.path.join(root, f)
            if os.path.isfile(file_path):
                if file_path.endswith(".dtd"):
                    file_path_key = file_path.split(path1)[1]
                    dtd_file_dict1[file_path_key] = dtd_parser.parse(file_path)
                if file_path.endswith(".properties"):
                    file_path_key = file_path.split(path1)[1]
                    properties_file_dict1[file_path_key] = properties_parser.parse(file_path)

    for root, dirs, files in os.walk(path2):
        for f in files:
            file_path = os.path.join(root, f)
            if os.path.isfile(file_path):
                if file_path.endswith(".dtd"):
                    file_path_key = file_path.split(path2)[1]
                    dtd_file_dict2[file_path_key] = dtd_parser.parse(file_path)
                if file_path.endswith(".properties"):
                    file_path_key = file_path.split(path2)[1]
                    properties_file_dict2[file_path_key] = properties_parser.parse(file_path)


    # here is the comparison
    dtd_keys1 = dtd_file_dict1.keys()
    dtd_keys2 = dtd_file_dict2.keys()

    for key in dtd_keys1:
        if key in dtd_keys2:
            dtd_value1 = dtd_file_dict1[key]
            dtd_value2 = dtd_file_dict2[key]

            value_diff = set(dtd_value1) - set(dtd_value2)

            if len(value_diff) > 0:
                logger.message("\t %s" % key)
                value_li = list(value_diff)
                for value in value_li:
                    logger.message("\t %s" % value)

    properties_keys1 = properties_file_dict1.keys()
    properties_keys2 = properties_file_dict2.keys()

    for key in properties_keys1:
        if key in properties_keys2:
            properties_value1 = properties_file_dict1[key]
            properties_value2 = properties_file_dict2[key]

            value_diff = set(properties_value1) - set(properties_value2)

            if len(value_diff) > 0:
                logger.message("\t %s" % key)
                value_li = list(value_diff)
                for value in value_li:
                    logger.message("\t %s" % value)
