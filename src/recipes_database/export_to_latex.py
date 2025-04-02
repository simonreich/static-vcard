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

class ExportToLatex(export_interface.ExportInterface, export_base.ExportBase):
    """
    This class exports a recipe class object to latex.

    Attributes:
        config (dict[str, str]): Dict holding all configuration. Should be directly passed from config.json.
        module_load (load_interface.LoadInterface): Object to use for loading data.
    """


    def __init__(self, config: dict[str, str], module_load: load_interface.LoadInterface):
        self.init(config, module_load)


    def beautify(self) -> None:
        """
        Performs latex beautifications of text.
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
                recipe.source = '\\url{' + recipe.source + '}{Internet}'


    def create_folder_structure(self) -> None:
        """
        Creates, and if necessary clears, target folders.
        """
        if self.config['delete_old_files']:
            self.helper.remove_file(self.path_to_out_main_file)
            self.helper.remove_folder(self.path_to_out_pages)

        self.helper.create_folder(self.path_to_out_main)
        self.helper.create_folder(self.path_to_out_pages)


    def export(self) -> None:
        """
        Main export routine.
        """
        self.create_folder_structure()

        self.export_pages()
        self.export_main()


    def export_pages(self):
        """
        Iterates over all recipes and creates one latex pages for each.

        In this function self.index_pages is built, which is used in export_main().
        """
        cnt = 0
        self.index_pages = {}

        # Loop over categories, then pages, then build index for latex main page
        for category in self.module_load.get_categories():
            self.index_pages[category] = []
            for recipe in self.module_load.get_recipies_by_category(category):
                path_to_file_out = join(self.path_to_out_pages, str(cnt) + '_' + category + '_' + recipe.name + '.tex')

                self.helper.write_template_to_file(self.path_to_page_template, path_to_file_out, {'recipe': recipe})

                self.index_pages[category].append(path_to_file_out)
                cnt = cnt + 1


    def export_main(self):
        """
        Builds the index for the main latex document.

        This function uses self.index_pages, which is built in export_pages().
        """
        indexstr = ''
        for category in self.index_pages.keys():
            indexstr += '\\section{' + category + '}\n'
            for path_to_file in self.index_pages[category]:
                indexstr += '\\newpage\n'
                indexstr += '\\input{' + path_to_file + '}\n'

        self.helper.write_template_to_file(self.path_to_main_template, self.path_to_out_main_file, {'index': indexstr})

