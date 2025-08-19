import json
import argparse
from os import listdir
from os.path import isdir, isfile, join, splitext, basename
from shutil import copytree


import sys
from pathlib import Path
sys.path.append(join(str(Path(__file__).absolute().parent.parent), 'helper'))
import helper

class StaticVcard:

    def __init__(self, path_to_config: str) -> None:
        self.helper = helper.Helper()

        # Load config
        self.load_config(path_to_config)

        # Export module
        self.build()

        print("done")


    def load_config(self, path_to_config):
        self.config = self.helper.get_dict_from_json(path_to_config)

        check_for_items = ['path_to_root', 'path_to_out', 'path_to_page_template', 'delete_old_files', 'rename_in_menu', 'deny_in_menu', 'min_length_in_menu']
        for item in check_for_items:
            if not item in self.config:
                raise KeyError('Section ' + item + ' not found in config file ' + path_to_config)

        self.path_to_root = self.config['path_to_root']
        self.path_to_out = self.config['path_to_out']
        self.path_to_page_template = self.config['path_to_page_template']
        self.delete_old_files = self.config['delete_old_files']
        self.rename_in_menu = self.config['rename_in_menu']
        self.deny_in_menu = self.config['deny_in_menu']
        self.min_length_in_menu = self.config['min_length_in_menu']

        self.folder_pages_generated = join(self.path_to_root, 'pages_generated')
        self.folder_pages_static = join(self.path_to_root, 'pages_static')
        self.folder_pages_temp = join(self.path_to_root, 'pages_temp')


    def build(self):
        self.create_folder_structure()
        self.copy_files_to_tempfolder()
        self.create_pagemap()
        self.create_menu()
        self.export()


    def create_folder_structure(self) -> None:
        """
        Creates, and if necessary clears, target folders.
        """
        if self.config['delete_old_files']:
            self.helper.remove_folder(self.path_to_out)
            self.helper.remove_folder(join(self.path_to_root, 'pages_temp'))

        self.helper.create_folder(self.path_to_out)
        self.helper.create_folder(join(self.path_to_root, 'pages_temp'))


    def copy_files_to_tempfolder(self) -> None:
        """
        Move pages from pages_static and pages_generated into pages_temp
        """
        copytree(self.folder_pages_generated, self.folder_pages_temp, dirs_exist_ok=True)
        copytree(self.folder_pages_static, self.folder_pages_temp, dirs_exist_ok=True)


    def sanitizeFilename(self, filename: str) -> str:
        """ Sanitizes a filename
            Input: string filename
            Return: string sanitized filename
        """
        filename = filename.lower()
        filename = filename.replace(" ", "-")
        return filename

    def create_pagemap(self) -> None:

        ## Create page list
        folders = [join(self.folder_pages_temp, f) for f in listdir(self.folder_pages_temp) if (isdir(join(self.folder_pages_temp, f)) and splitext(str(f))[1][1:].isdigit())]
        folders = sorted(folders, key=lambda x: int(splitext(x)[1][1:]))

        self.map_of_pages = []
        for folder in folders:
            path_to_folder_in = folder
            filename_out = self.sanitizeFilename(self.helper.remove_file_extension(self.helper.remove_path(folder)))
            name = self.helper.remove_file_extension(self.helper.remove_file_extension(self.helper.remove_path(folder)))

            # Second level
            files = [join(folder, f) for f in listdir(folder) if splitext(str(f))[1][1:].isdigit()]
            files = sorted(files, key=lambda x: int(splitext(x)[1][1:]))
         
            sections = []
            for file in files:
                path_to_file_in = file
                name2 = self.helper.remove_file_extension(self.helper.remove_path(file))
                anchor2 = name2.lower()
                url2 = filename_out + '#' + anchor2
                html2 = self.helper.read_from_file(path_to_file_in)
         
                sections.append({
                    'path_to_file_in': path_to_file_in,
                    'name': name2,
                    'url': url2,
                    'html': html2,
                    'anchor': anchor2
                    })
         
            self.map_of_pages.append({
                'path_to_folder_in': path_to_folder_in,
                'filename_out': filename_out,
                'name': name,
                'sections': sections
                })


    def create_menu(self) -> None:
        self.map_of_menu = []
        self.map_of_menu_sections = {}
        for page in self.map_of_pages:
            name = page['name']
            if name.lower() in self.rename_in_menu.keys():
                name = self.rename_in_menu[name.lower()]

            sections = []
            if len(page['sections']) > self.min_length_in_menu:
                for section in page['sections']:
                    sections.append({
                        'name': section['name'],
                        'url': section['url']
                        })

            if name.lower() not in self.deny_in_menu:
                self.map_of_menu.append({
                    'name': name,
                    'url': page['filename_out'],
                    'sections': sections
                    })
            self.map_of_menu_sections[page['name']] = sections


    def export(self) -> None:
        for page in self.map_of_pages:
            path_to_file_out = join(self.path_to_out, page['filename_out'])

            # 1. Build pages via template
            self.helper.write_template_to_file(self.path_to_page_template, path_to_file_out, 
                                               {'map_of_pages': self.map_of_pages, 
                                                'sections': page['sections'], 
                                                'map_of_menu': self.map_of_menu, 
                                                'map_of_menu_sections': self.map_of_menu_sections[page['name']],
                                                'compile_timestap': self.helper.get_timestamp()
                                               })

            # 2. Use page as template for inline replacements
            self.helper.write_template_to_file(path_to_file_out, path_to_file_out, 
                                               {'map_of_pages': self.map_of_pages, 
                                                'sections': page['sections'], 
                                                'map_of_menu': self.map_of_menu, 
                                                'map_of_menu_sections': self.map_of_menu_sections[page['name']],
                                                'compile_timestap': self.helper.get_timestamp()
                                               })

        copytree(join(self.path_to_root, 'static'), 'out', dirs_exist_ok=True)


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

    rd = StaticVcard(config_file)


if __name__ == "__main__":
    # execute only if run as a script
    main()

