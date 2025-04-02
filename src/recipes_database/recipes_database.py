import json
import argparse

import sys
from pathlib import Path
from os.path import join
sys.path.append(join(str(Path(__file__).absolute().parent.parent), 'helper'))
import helper

import load_from_json
import export_to_latex
import export_to_html
import load_interface
import export_interface

class RecipesDatabase:

    def __init__(self, path_to_config: str) -> None:
        self.helper = helper.Helper()

        # Load config
        self.load_config(path_to_config)

        # Load module
        self.load()

        # Export module
        self.export()

        print("done")


    def load_config(self, path_to_config):
        self.config = self.helper.get_dict_from_json(path_to_config)

        check_for_items = ["module_load", "module_export", self.config["module_load"], self.config["module_export"]]
        for item in check_for_items:
            if not item in self.config:
                raise KeyError('Section ' + item + ' not found in config file ' + path_to_config)
        return


    def load(self):
        if self.config['module_load'].lower() == "load_from_json":
            self.module_load = load_from_json.LoadFromJson(self.config['load_from_json'])
        return


    def export(self):
        if self.config['module_export'].lower() == "export_to_latex":
            self.module_load = export_to_latex.ExportToLatex(self.config['export_to_latex'], self.module_load)
        if self.config['module_export'].lower() == "export_to_html":
            self.module_load = export_to_html.ExportToHtml(self.config['export_to_html'], self.module_load)
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Json config file.")
    args = parser.parse_args()

    config_file = None
    if args.c:
        config_file = args.c
    else:
        print('No config file given.')
        raise

    rd = RecipesDatabase(config_file)


if __name__ == "__main__":
    # execute only if run as a script
    main()

