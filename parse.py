import sys
import os

class FileHandler:

    def __init__(self):
        self.f = None

    def set_file(self, filename):
        self.f = file(self.filename)

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
    dtd_file_dict = dict()

    properties_parser = PropertiesParser()
    properties_file_dict = dict()

    path1 = sys.argv[1]
    path2 = sys.argv[2]

    for root, dirs, files in os.walk(path1):
        if os.path.isfile(root):
            if root.endswith(".dtd"):
                dtd_file_dict[root] = dtd_parser.parse(root)
            if root.endswith(".properties"):
                properties_file_dict[root] = properties_parser.parse(root)

    # here is the comparison

