#! /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Copyright (C) 2023 Simon Reich. Licensed under the GPL (see the license file).

This program reads a folder and creates for every static-vcard page an entry in a table of contents.
"""


import argparse
from os import listdir, path, makedirs 


class createtoc:
    def run(self, folderIn, fileOut):
        # List of valid index pages
        validIndexPage = ['index.html', 'index.htm', 'index.php']

        # List of valid impressum pages
        validImpressumPage = ['impressum.html', 'impressum.htm', 'impressum.php']

        # Working dir
        folderPages = path.join(folderIn, 'pages')

        # Create page list
        pages = [f for f in listdir(folderPages) if (path.isdir(path.join(folderPages, f)) and path.splitext(str(f))[1][1:].isdigit())]
        pages = sorted(pages, key=lambda x: int(path.splitext(x)[1][1:]))
 
        # HTML for this page
        pageHtml = ''

        # Create single page
        for page in pages:

            # Remove integer from file path
            pagePath = path.splitext(page)[0]
            pageName = path.splitext(pagePath)[0]

            # Do not add index or impressum
            if pagePath.lower() in validIndexPage or pagePath.lower() in validImpressumPage:
                continue
 
            # Read sections
            sections = [f for f in listdir(path.join(folderPages, page)) if path.isfile(path.join(folderPages, page, f)) and path.splitext(str(f))[1][1:].isdigit()]
            sections = sorted(sections, key=lambda x: int(path.splitext(x)[1][1:]))

            # Create HTML
            pageHtml += '<h3>' + pageName + '</h3>\n<ul>\n'

            counter = 0
            for section in sections:
                pageHtml += '  <li><a href="' + pageName.lower() + '.html#' + str(path.splitext(section)[0]).lower() + '">' + str(path.splitext(section)[0]) + '</a></li>\n'
                counter += 1

            pageHtml += '</ul>\n'

        # Write results
        f = open(fileOut, "w")
        f.write(pageHtml)
        f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder holding static-vcard pages files ~/something/pages.")
    parser.add_argument("-o", help="Output file for HTML.")
    args = parser.parse_args()

    folderIn = None
    if args.i:
        folderIn = args.i
    else:
        print('No input folder given.')
        raise

    fileOut = None
    if args.o:
        fileOut = args.o
    else:
        print('No output file given.')
        raise

    Createtoc = createtoc()
    Createtoc.run(folderIn, fileOut)


if __name__ == "__main__":
    # execute only if run as a script
    main()
