# -*- coding: utf-8 -*-


"""
Copyright (C) 2023 Simon Reich. Licensed under the GPL (see the license file).

This program reads a folder and creates for every xcookybooky recipe it finds, an html page.
"""


import argparse
import os
import shutil


class xcookybooky2html:
    def run(self, folderIn, folderOut):
        # Read file list *tex
        filenames = [os.sep.join([folderIn, f]) for f in os.listdir(folderIn) if os.path.isfile(os.sep.join([folderIn, f])) and os.path.splitext(f)[1] == ".tex"]

        # Folders that are created
        foldersCreated = {}

        for filename in filenames:
            # Run
            results = self.processOneFile(filename)

            # Create output folder - 1st level
            folderOutPath = os.sep.join([folderOut, os.path.basename(filename).split("_")[0].capitalize()])
            if not os.path.exists(folderOutPath):
                os.mkdir(folderOutPath)
            if folderOutPath not in foldersCreated:
                foldersCreated[folderOutPath] = []

            # Write to file
            fileOut = os.sep.join([folderOutPath, results["header"]])
            f = open(fileOut, "w")
            f.write(self.convertResultsToHtml(results))
            f.close()

            foldersCreated[folderOutPath].append(fileOut)

        # static-vcard needs enumeration and extension of pages to be created
        self.renameFilesAndFolders(foldersCreated)


    def processOneFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        text = ("".join(lines))

        # Extract Text blocks
        textPieces = self.getFirstLevel(text)

        # Sanitize
        results = {
                "header":self.extractHeader(textPieces[2]),
                "metainfo":self.extractMetainfo(textPieces[1]),
                "ingredients":self.extractIngredients(textPieces[3]),
                "steps":self.extractSteps(textPieces[4])
                }

        # Check for hints
        if len(textPieces) > 6:
            results["hints"] = self.extractSteps(textPieces[5])

        return results


    def renameFilesAndFolders(self, foldersCreated):
        cntFolder = 1
        for (folder, filenames) in sorted(foldersCreated.items()):
            # Enumerate files inside folder
            cntFile = 1
            for filename in sorted(foldersCreated[folder]):
                filenameFrom = filename
                filenameTo = filename + '.' + str(cntFile)
                if os.path.isfile(filenameTo):
                    os.remove(filenameTo)
                os.rename(filenameFrom, filenameTo)
                cntFile += 1

            # Enumerate folder
            folderPathFrom = folder
            folderPathTo = folder + '.html.' + str(cntFolder)
            if os.path.isdir(folderPathTo):
                shutil.rmtree(folderPathTo)
            os.rename(folderPathFrom, folderPathTo)
            cntFolder += 1


    def convertResultsToHtml(self, results):
        html = ''
        metainfo = self.createHtmlTable(results["metainfo"])
        ingredients = self.createHtmlTable(results["ingredients"])
        steps = self.createHtmlOl(results["steps"])

        html += metainfo + '\n'
        html += '<h3>Zutaten</h3>\n' + ingredients + '\n'
        html += '<h3>Zubereitung</h3>\n' + steps + '\n'

        if "hints" in results:
            hints = self.createHtmlOl(results["hints"])
            html += '<h3>Tipps</h3>\n' + hints + '\n'

        return html
        


    def getFirstLevel(self, text):
        indices = self.getIndices(text)

        currentStartIndex = -1
        currentTyp = ""
        currentState = "close"
        BracketCounter = 0
        textPiecesIndices = []

        for i in range(len(indices)):
            pos = indices[i][0]
            typ = indices[i][2]
            state = indices[i][3]

            if currentState == "close" and state == "open":
                currentStartIndex = i
                currentTyp = typ
                currentState = state
                continue


            if currentState == "open" and state == "open" and currentTyp == typ:
                BracketCounter += 1
                continue

            if currentState == "open" and state == "close" and currentTyp == typ and BracketCounter > 0:
                BracketCounter -= 1
                continue

            if currentState == "open" and state == "close" and currentTyp == typ and BracketCounter == 0:
                currentState = state
                textPiecesIndices.append((indices[currentStartIndex], indices[i]))
                continue

        textPieces = [text[x[0][0]+1:x[1][0]] for x in textPiecesIndices]

        return textPieces


    def getIndices(self, text):
        indices = [(i, text[i]) for i in range(len(text)) if text[i] in ["{", "}", "[", "]"]]
        indices = [(x[0], x[1], "curly") if x[1] in ["{", "}"] else (x[0], x[1], "square") for x in indices]
        indices = [(x[0], x[1], x[2], "open") if x[1] in ["{", "["] else (x[0], x[1], x[2], "close") for x in indices]
        return indices


    def extractHeader(self, text):
        header = ""
        if "label" in text:
            header = text[0:text.index("\\label")].strip()
        else:
            header = text.strip()

        return self.cleanLatex(header)


    def extractSteps(self, text):
        clean = [self.cleanLatex(x) for x in text.split("\n")]
        clean = [x for x in clean if len(x) > 5]
        return clean


    def extractIngredients(self, text):
        clean = [self.cleanLatex(x) for x in text.split("\n")]
        clean = [x for x in clean if len(x) > 2]
        clean = [x.split("&") for x in clean]
        f = lambda x : [y.strip() for y in x]
        clean = [f(x) for x in clean]
        return clean

        
    def extractMetainfo(self, text):
        clean = [self.cleanLatex(x) for x in text.split("\n")]
        clean = [x for x in clean if len(x) > 5]
        clean = [x.replace(",", "") for x in clean]
        clean = [x.split("=") for x in clean]
        f = lambda x : [y.strip() for y in x]
        clean = [f(x) for x in clean]
        return clean


    def cleanLatex(self, text):
        text = text.replace("\\frac", "")
        text = text.replace("\\step", "")
        text = text.replace("\\unit[", "")
        text = text.replace("]{", " ")
        text = text.replace("}", "")
        text = text.replace("{", "")
        text = text.replace('\"O', "Ö")
        text = text.replace('\"U', "Ü")
        text = text.replace('\"A', "Ä")
        text = text.replace('\"o', "ö")
        text = text.replace('\"u', "ü")
        text = text.replace('\"a', "ä")
        text = text.replace("\\ss\\", "ß ")
        text = text.replace("\\ss ", "ß")
        text = text.replace("\\ss", "ß")
        text = text.replace("\\\\", "")
        text = text.replace("\\portion", "")
        text = text.replace("\\url", "")
        text = text.replace(" \\textcelcius", "°")
        text = text.replace("\\textcelcius", "°")
        text = text.replace("\\`e", "è")
        text = text.replace("\\´e", "é")
        text = text.replace("\\`e", "è")
        text = text.replace("\\^a", "â")
        text = text.replace("\\^e", "ê")
        text = text.replace("\\^i", "î")
        text = text.replace("\\^o", "ô")
        text = text.replace("\\^u", "û")
        text = text.replace("\\", "")
        text = text.replace("$", "")
        text = text.replace("--", "–")
        text = text.replace("preparationtime", "Vorbereitungszeit")
        text = text.replace("portion", "Portion")
        text = text.replace("calory", "Kalorien")
        text = text.replace("source", "Quelle")
        text = text.replace("bakingtime", "Backzeit")
        text = text.replace("bakingtemperature", "Temperatur")
        return text.strip()


    def createHtmlTable(self, lines):
        ## Generate HTML
        strOut = '<table>\n'
        for line in lines:
            strOut += '  <tr>\n'
            for item in line:
                if "http" in item:
                    itemtext = '<a href="' + item + '">Internet</a>'
                else:
                    itemtext = item

                strOut += '    <td>' + itemtext + '</td>\n'
            strOut += '  </tr>\n'
        
        strOut += '</table>\n'
        return strOut


    def createHtmlOl(self, lines):
        ## Generate HTML
        strOut = '<ol>\n'
        for line in lines:
            strOut += '  <li>' + line + '</li>\n'

        strOut += '</ol>\n'
        return strOut


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder holding xcookybooky files.")
    parser.add_argument("-o", help="Output folder ~/something/pages.")
    args = parser.parse_args()

    folderIn = None
    if args.i:
        folderIn = args.i
    else:
        print('No input folder given.')
        raise

    folderOut = None
    if args.o:
        folderOut = args.o
    else:
        print('No output folder given.')
        raise

    Xcookybooky2html = xcookybooky2html()
    Xcookybooky2html.run(folderIn, folderOut)


if __name__ == "__main__":
    # execute only if run as a script
    main()
