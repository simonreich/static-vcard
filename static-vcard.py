#! /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Copyright (C) 2018 Simon Reich. Licensed under the GPL (see the license file).

This program reads 
    template/header.html
    template/footer.html
    pages/*/*.n
    static/*

where n is an integer >=0. 
The example page out/name-of-page.html will be formatted as
    template/header.html
    pages/name-of-page.html/*.0
    pages/name-of-page.html/*.1
    pages/name-of-page.html/*.2
    ...
    template/footer.html

The resulting files will be placed in folder out/.
"""


from os import listdir, path, makedirs 
from distutils.dir_util import copy_tree


if __name__ == '__main__':
    ## List of valid index pages
    validIndexPage = ['index.html', 'index.htm', 'index.php']


    ## Read header
    headerFile = open('template/header.html', 'r')
    headerHtml = headerFile.read()


    ## Read footer
    footerFile = open('template/footer.html', 'r')
    footerHtml = footerFile.read()

 
    ## Create out folder
    if path.exists('out') == False:
        makedirs('out')
    else:
        if path.isdir('out') == False:
            raise('File "out" exists, but should be a folder.')


    ## Create page list
    pages = [f for f in listdir('pages') if path.isdir(path.join('pages', f))]


    ## Find name of index page
    pageIndex = ''
    for page in pages:
        if (str(page) == 'index.html') or (str(page) == 'index.htm') or (str(page) == 'index.php'):
            pageIndex = page


    ## Create single page
    for page in pages:
        pageHtml = ''

        ## Read sections
        sections = [f for f in listdir('pages/' + str(page)) if (path.isfile(path.join('pages/' + str(page), f)) and path.splitext(str(f))[1][1:]).isdigit()]
        sections = sorted(sections, key=lambda x: path.splitext(x)[1])

        ## Create page index
        if page not in validIndexPage:
            if str(pageIndex) != '':
                pageHtml += '<a href="' + str(pageIndex) + '">Home</a>'
                if len(sections) > 1:
                    pageHtml += ' • '

        counter = 0
        if len(sections) > 1:
            for section in sections:
                pageHtml += '<a href="#' + str(path.splitext(section)[0]).lower() + '">' + str(path.splitext(section)[0]) + '</a>'
                if counter < len(sections)-1:
                    pageHtml += ' • '
                counter += 1

        pageHtml += '\n\n<hr />\n\n'


        ## Create sections
        for section in sections:
            pageHtml += '<a name="' + str(path.splitext(section)[0]).lower() + '"></a>\n'
            pageHtml += '<h2>' + str(path.splitext(section)[0]) + '</h2>\n\n'
            sectionFile = open('pages/' + page + '/' + section, 'r')
            pageHtml += sectionFile.read()
 
            pageHtml += '\n<a href="#top">top</a><hr />\n\n'
 
        ## Write to file
        fileIndex = open('out/' + page, 'w') 
        fileIndex.write(headerHtml) 
        fileIndex.write(pageHtml) 
        fileIndex.write(footerHtml) 
        fileIndex.close() 

    ## Copy static folder
    copy_tree('static', 'out', update=1)
