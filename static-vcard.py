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


def sanitizeFilename(_filename):
    """ Sanitizes a filename
        Input: string filename
        Return: string sanitized filename
    """
    filename= _filename.lower()
    filename = filename.replace(" ", "-")
    return filename


if __name__ == '__main__':
    ## List of valid index pages
    validIndexPage = ['index.html', 'index.htm', 'index.php']


    ## List of valid impressum pages
    validImpressumPage = ['impressum.html', 'impressum.htm', 'impressum.php']


    ## Read header
    headerFile = open('template/header.html', 'r')
    headerHtml = headerFile.read()
    headerFile.close()


    ## Read footer
    footerFile = open('template/footer.html', 'r')
    footerHtml = footerFile.read()
    footerFile.close()

 
    ## Create out folder
    if path.exists('out') == False:
        makedirs('out')
    else:
        if path.isdir('out') == False:
            raise('File "out" exists, but should be a folder.')


    ## Create page list
    pages = [f for f in listdir('pages') if (path.isdir(path.join('pages', f)) and path.splitext(str(f))[1][1:].isdigit())]
    pages = sorted(pages, key=lambda x: int(path.splitext(x)[1][1:]))


    ## Create single page
    for page in pages:
        ## Remove integer from file path
        pagePath = path.splitext(page)[0]
        pageName = path.splitext(pagePath)[0]

        ## Sanity path
        pagePath = sanitizeFilename(pagePath)

        ## HTML for this page
        pageHtml = ''

        ## Read sections
        sections = [f for f in listdir('pages/' + str(page)) if (path.isfile(path.join('pages/' + str(page), f)) and path.splitext(str(f))[1][1:].isdigit())]
        sections = sorted(sections, key=lambda x: int(path.splitext(x)[1][1:]))

        ## Create page index
        counter = 0
        if len(pages) > 2:
            for page1 in pages:
                ## Remove integer from file path
                page1Path = path.splitext(page1)[0]
                page1Name = path.splitext(page1Path)[0]
        
                ## Sanity path
                page1Path = sanitizeFilename(page1Path)

                if page1Path.lower() not in validImpressumPage:
                    if page1Path.lower() in validIndexPage:
                        pageHtml += '<a href="' + str(page1Path) + '">Home</a>'
                    else:
                        pageHtml += '<a href="' + str(page1Path) + '">' + str(page1Name) + '</a>'
                    if counter < len(pages)-2:
                        pageHtml += ' • '
                counter += 1
            pageHtml += '\n\n<br /><br />\n\n'
        else:
            ## Remove integer from file path
            page1Path = path.splitext(page1)[0]
            page1Name = path.splitext(page1Path)[0]
            if page1Path.lower() not in validIndexPage:
                pageHtml += '<a href="' + str(page1Path) + '">Home</a>'
                if len(sections) > 1:
                    pageHtml += ' • '


        ## Create section index
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
            sectionFile.close()
 
            pageHtml += '\n<a href="#top">top</a><hr />\n\n'
 
        ## Write to file
        fileIndex = open('out/' + pagePath, 'w') 
        fileIndex.write(headerHtml) 
        fileIndex.write(pageHtml) 
        fileIndex.write(footerHtml) 
        fileIndex.close() 

    ## Copy static folder
    copy_tree('static', 'out', update=1)
