from abc import ABC, abstractmethod
import typing
from os.path import join

import sys
from pathlib import Path
sys.path.append(join(str(Path(__file__).absolute().parent.parent), 'helper'))
import helper

import recipe 
import load_interface

class LoadFromJson(load_interface.LoadInterface):


    def __init__(self, config: dict[str, str]):
        self.helper = helper.Helper()
        self.config = config
        self.check_config()
        self.load_db_from_path(config["path_to_json_files"])


    def get_recipies(self):
        return self.recipies


    def get_recipies_by_name(self, name: str):
        recipies = [recipe for recipe in self.recipies if recipe.name == name]
        return recipies


    def get_names(self):
        return [recipe.name for recipe in self.recipies]


    def get_recipies_by_category(self, category: str):
        recipies = [recipe for recipe in self.recipies if recipe.category == category]
        return recipies


    def get_categories(self):
        return sorted(list(set([recipe.category for recipe in self.recipies])))


    def get_recipies_by_tag(self, tag: str):
        recipies = [recipe for recipe in self.recipies if tag in recipe.tags]
        return recipies


    def get_tags(self):
        tags = []
        [tags.extend(recipe.tags) for recipe in self.recipies]
        return sorted(list(set(tags)))


    def get_tags_as_dict(self):
        tags = {}
        for tag in self.get_tags():
            tags[tag] = self.get_recipies_by_tag(tag)
        return tags


    def check_config(self):
        check_for_items = ["path_to_json_files"]
        for item in check_for_items:
            if not item in self.config:
                raise KeyError('Section ' + item + ' not found in config file.')


    def load_db_from_path(self, path_to_json_files: str):
        files = self.helper.get_list_of_files(path_to_json_files, ".json")

        self.recipies = []
        for file in files:
            jsonstring = self.helper.get_dict_from_json(join(path_to_json_files, file))
            root = recipe.Root(**jsonstring)
            
            self.recipies.append(root)

        self.recipies = sorted(self.recipies, key=lambda d: d.name)

