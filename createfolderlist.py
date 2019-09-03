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
    ''' Returns a list of all files containing in folder folder.
        List is sorted alphanumerical.
    '''

    filelist = []
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            #filename = os.path.join(folder, filename)
            filelist.append(filename)

    filelist = sorted(filelist)
    if debug: print('Loaded list holding ' + str(len(filelist)) + ' files.')

    return filelist



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

    ## List of valid index pages
    filelist = getFilelist(folderIn, True)

    strOut = '<ul>\n'
    for filename in filelist:
        name = filename[:-4]
        name = name.split('_')
        date = name[0].split('-')
        strOut += '<li><a href=\"/' + str(filename) + '\">'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 0:
            strOut += 'Montag'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 1:
            strOut += 'Dienstag'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 2:
            strOut += 'Mittwoch'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 3:
            strOut += 'Donnerstag'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 4:
            strOut += 'Freitag'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 5:
            strOut += 'Samstag'
        if datetime.datetime(int(date[0]), int(date[1]), int(date[2])).weekday() == 6:
            strOut += 'Sonntag'
        strOut += ', ' + str(date[2]) + '.' + str(date[1]) + '.' + str(date[0])

        if len(name) > 1:
            strOut += ' (' + str(name[1]).capitalize() + ')'

        strOut += '</a></li>\n'
    strOut += '</ul>\n'

    # Write to file
    fp = open(fileOut, 'w')
    fp.write(strOut)
    fp.close()
