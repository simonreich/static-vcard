from os.path import basename, join

import sys
from pathlib import Path
from os.path import join
sys.path.append(join(str(Path(__file__).absolute().parent.parent), 'helper'))
import helper

import export_interface
import load_interface

class ExportBase():

    def init(self, config: dict[str, str], module_load: load_interface.LoadInterface):
        """
        Init function, because calling super() with multiple inheritances is difficult.

        Attributes:
            config (dict[str, str]): Dict holding all configuration. Should be directly passed from config.json.
            module_load (load_interface.LoadInterface): Object to use for loading data.
        """
        self.helper = helper.Helper()
        self.module_load = module_load

        self.config = config
        self.check_config()
        self.get_paths_from_config()

        self.beautify()
        self.export()


    def check_config(self) -> None:
        """
        Checks if necessary keys in config dict are present.
        """
        check_for_items = ['path_to_out_main', 'path_to_out_pages', 'delete_old_files', 'path_to_main_template', 'path_to_page_template']
        for item in check_for_items:
            if not item in self.config:
                raise KeyError('Section ' + item + ' not found in config file.')


    def get_paths_from_config(self) -> None:
        """
        Builds all necessary paths from config dict.
        """
        self.path_to_main_template = self.config['path_to_main_template']
        self.path_to_page_template = self.config['path_to_page_template']
        self.path_to_out_main = self.config['path_to_out_main']
        self.path_to_out_pages = self.config['path_to_out_pages'] 

        self.filename_out_main = self.helper.remove_file_extension(basename(self.config['path_to_main_template']))
        self.path_to_out_main_file = join(self.path_to_out_main, self.filename_out_main)
