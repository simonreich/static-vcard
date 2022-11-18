#! /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Copyright (C) 2019 Simon Reich. Licensed under the GPL (see the license file).

This program reads a folder given by -i parameter and outputs a list of pdf found pdf files into a file specified by the -o parameter
"""


import os
from distutils.dir_util import copy_tree
import datetime
import argparse



def getFilelist (folder, debug=False):
    ''' Returns a list of all files in folder.
        List is sorted alphanumerical.
    '''

    filelist = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        filelist+= [os.path.join(dirpath, file) for file in filenames]

    filelist = sorted(filelist)
    if debug: print('Loaded list holding ' + str(len(filelist)) + ' files.')

    return filelist



def getExtensiondictFromFilelist (filelist):
    ''' Returns a list of file extensions (everything after the ".") given a list of files.
    '''

    extensionlist = [os.path.splitext(x)[1][1:] for x in filelist]
    extensiondict = dict.fromkeys(extensionlist, 0)
    
    return extensiondict



def getDescriptiondict():
    ''' Returns a dict of descriptions to file extensions.
    '''

    description =  {
        "jpg": "Pictures",
        "jpeg": "Pictures",
        "png": "Pictures",
        "pdf": "PDF-files",
        "htm": "HTML",
        "html": "HTML",
        "php": "PHP",
        "css": "CSS",
        "js": "Java Script",
        "mp4": "Video",
        "asc": "PGP Key"
        }

    return description



def getUnits(descriptionAndFilesizesList):
    ''' Reads a list of tupels [('Description', Filesizes)] and returns a list of tupels where Filesizes contains the size unit.
    '''

    unit = {
        0: "Bytes",
        1: "KB",
        2: "MB",
        3: "GB",
        4: "TB"
        }
    

    descriptionAndFilesizesWithUnitList = []    
    for (key, value) in descriptionAndFilesizesList:
        newValue = value
        cnt = 0
        while(newValue > 1024):
            newValue /= 1024
            cnt += 1

        descriptionAndFilesizesWithUnitList.append((key, str(round(newValue, 1)) + " " + unit[cnt]))

    return descriptionAndFilesizesWithUnitList



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder, must contain pdf files.")
    parser.add_argument("-o", help="Output file, html formatted.")
    args = parser.parse_args()
    folderIn = args.i
    fileOut = args.o

    if (folderIn == None) or (fileOut == None):
        print('Please specify -i and -o option.')
        raise

    print(folderIn)

    ## List of valid index pages
    filelist = getFilelist(folderIn, True)

    ## List of extensions
    extensiondict = getExtensiondictFromFilelist(filelist)

    ## Compute file sizes in bytes and add to dict
    for filename in filelist:
        fileExt = os.path.splitext(filename)[1][1:]
        fileStats = os.stat(filename)
        extensiondict[fileExt] += fileStats.st_size

    ## Transfer from extension to description dict
    descriptionAndFilesizesDict = {}
    for key in extensiondict.keys():
        newKey = ""
        if key in getDescriptiondict():
            newKey = getDescriptiondict()[key]
        else:
            newKey = "Misc"

        if newKey in descriptionAndFilesizesDict:
            descriptionAndFilesizesDict[newKey] += extensiondict[key]
        else:
            descriptionAndFilesizesDict[newKey] = extensiondict[key]

    ## Sort dict
    descriptionAndFilesizesList = sorted(descriptionAndFilesizesDict.items(), key=lambda x: x[1], reverse=True)

    ## Add units
    descriptionAndFilesizesWithUnitList = getUnits(descriptionAndFilesizesList)

    ## Generate HTML
    strOut = '<table>\n  <tr>\n    <th>Files</th>\n    <th>Sizes</th>\n  </tr>\n'
    for (key, value) in descriptionAndFilesizesWithUnitList:
        strOut += '  <tr>\n    <td>' + key + '</td>\n    <td>' + value + '</td>\n  </tr>\n'

    strOut += '</table>\n'

    # Write to file
    fp = open(fileOut, 'w')
    fp.write(strOut)
    fp.close()
