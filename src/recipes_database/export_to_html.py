from abc import ABC, abstractmethod
import typing
from os.path import join, splitext

import sys
from pathlib import Path
sys.path.append(join(str(Path(__file__).absolute().parent.parent), 'helper'))
import helper

import recipe 
import export_base
import export_interface
import load_interface

class ExportToHtml(export_interface.ExportInterface, export_base.ExportBase):
    """
    This class exports a recipe class object to html.

    Attributes:
        config (dict[str, str]): Dict holding all configuration. Should be directly passed from config.json.
        module_load (load_interface.LoadInterface): Object to use for loading data.
    """


    def __init__(self, config: dict[str, str], module_load: load_interface.LoadInterface):
        self.init(config, module_load)


    def beautify(self) -> None:
        """
        Performs html beautifications of text.
        """
        def replace_dash(text: str) -> str:
            return text.replace(' ', '').replace('-', ' -- ')

        for recipe in self.module_load.get_recipies():
            # Replace hyphen with dashes
            recipe.preparation_time_minutes = replace_dash(recipe.preparation_time_minutes)
            recipe.baking_time_minutes = replace_dash(recipe.baking_time_minutes)
            recipe.baking_temperature_celcius = replace_dash(recipe.baking_temperature_celcius)
            recipe.cooking_time_minutes = replace_dash(recipe.cooking_time_minutes)
        
            # Replace html source
            if 'http' in recipe.source.lower():
                recipe.source = '<a href="' + recipe.source + '">Internet</a>'


    def create_folder_structure(self) -> None:
        """
        Creates, and if necessary clears, target folders.
        """
        if self.config['delete_old_files']:
            self.helper.remove_folder(self.path_to_out_pages)

        self.helper.create_folder(self.path_to_out_pages)

        self.page_folders = {
                'index': join(self.path_to_out_pages, 'index.html.0'), 
                }
        cnt = 1
        for category in self.module_load.get_categories():
            self.page_folders[category] = join(self.path_to_out_pages, category + '.html.' + str(cnt))
            cnt += 1

        for page_folder in self.page_folders.keys():
            self.helper.create_folder(self.page_folders[page_folder])


    def export(self) -> None:
        """
        Main export routine.
        """
        self.create_folder_structure()

        self.export_pages()
        self.export_main()


    def export_pages(self):
        """
        Iterates over all recipes and creates one html pages for each.

        In this function self.index_pages is built, which is used in export_main().
        """
        cnt = 0
        self.index_pages = {}

        # Loop over categories, then pages, then build index for html main page
        for category in self.module_load.get_categories():
            self.index_pages[category] = []
            for recipe in self.module_load.get_recipies_by_category(category):
                path_to_file_out = join(self.page_folders[category], recipe.name + '.' + str(cnt))

                self.helper.write_template_to_file(self.path_to_page_template, path_to_file_out, {'recipe': recipe})

                self.index_pages[category].append({
                    'folder': self.page_folders[category], 
                    'full_path': path_to_file_out, 
                    'filename': recipe.name + '.' + str(cnt),
                    'name': recipe.name})
                cnt = cnt + 1


    def export_main(self):
        """
        Builds the index for the main html document.

        This function uses self.index_pages, which is built in export_pages().
        """
        #path_to_file_out = join(self.page_folders['index'], 'Version.3')
        #timestamp = self.helper.get_timestamp()
        #self.helper.write_template_to_file(self.path_to_main_template, path_to_file_out, {'timestamp': timestamp})
        pass

