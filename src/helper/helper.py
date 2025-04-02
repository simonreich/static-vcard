import json
from os import listdir, makedirs, remove
from os.path import isdir, isfile, join, splitext, basename
from shutil import rmtree
import datetime
from jinja2 import Template, Environment, PackageLoader, select_autoescape

class Helper:

    def init(self) -> None:
        pass

    def get_dict_from_json (self, path_to_json: str) -> str:
        with open(path_to_json) as f:
            d = json.load(f)
        return d


    def get_list_of_files(self, path: str, ext: str = None) -> list[str]:
        return [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(ext)]


    def create_folder(self, path: str) -> None:
        if not isdir(path):
            makedirs(path)
        return


    def remove_file(self, path: str) -> None:
        if isfile(path):
            remove(path)
        return


    def remove_folder(self, path: str) -> None:
        if isdir(path):
            rmtree(path)
        return


    def write_template_to_file(self, 
                               path_to_template: str, 
                               path_to_file_out: str, 
                               replacement: dict) -> None:
        with open(path_to_template) as f:
            template = Template(f.read())
        self.write_string_to_file(path_to_file_out, template.render(replacement))
        return


    def write_string_to_file(self, path_to_file: str, text :str) -> None:
        with open(path_to_file, 'w') as f:
            f.write(text)


    def read_from_file(self, path_to_file: str) -> str:
        with open(path_to_file, 'r') as f:
            string = f.read()
        return string


    def remove_file_extension(self, filename: str) -> str:
        root, ext = splitext(filename)
        return root


    def remove_path(self, path_with_filename: str) -> str:
        return basename(path_with_filename)


    def get_timestamp(self) -> str:
        return str(datetime.datetime.now())

