# -*- coding: utf-8 -*-
"""
This file is part of swarmcontrol.
swarmcontrol is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
swarmcontrol is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with swarmcontrol.  If not, see <http://www.gnu.org/licenses/>.
"""



import argparse
import os


class xcookybooky2html:
    def run(self, folderIn, folderOut):
        # Read file list
        filenames = os.listdir(folderIn)

        cnt = 1
        for filename in filenames:
            # Run
            results = processOneFile(filename)

            # Create output folder
            folderOut = os.sep.join([folderOut, os.path.basename(filename).split("_")[0].capitalize()])
            if not os.path.exists(folderOut):
                os.mkdir(folderOut)
            folderOut = os.sep.join([folderOut, result[0] + ".html" + str(cnt)])
            if not os.path.exists(folderOut):
                os.mkdir(folderOut)

            # Write to file
            fileOut = os.sep.join([folderOut, filename])
            f = open("Infos", "w")
            f.write("Woops! I have deleted the content!")
            f.close()

            cnt += 1

    def processOneFile(self, filename)
        with open(filename) as f:
            lines = f.readlines()
        text = ("".join(lines))

        # Extract Text blocks
        textPieces = self.getFirstLevel(text)

        # Sanitize
        header = self.extractHeader(textPieces[2])
        metainfo = self.extractMetainfo(textPieces[1])
        ingredients = self.extractIngredients(textPieces[3])
        steps = self.extractSteps(textPieces[4])

        return [header, metainfo, ingredients, steps]
        


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

            print(i, typ, currentTyp, state, currentState, BracketCounter)

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
        if "label" in text:
            return text[0:text.index("\\label")].strip()
        else:
            return text.strip()

    def extractSteps(self, text):
        clean = [self.cleanLatex(x) for x in text.split("\n")]
        clean = [x for x in clean if len(x) > 5]
        return clean


    def cleanLatex(self, text):
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
        text = text.replace("\\ss", "ß")
        text = text.replace("\\ss", "ß ")
        text = text.replace("\\\\", "")
        text = text.replace("\\portion", "")
        text = text.replace("\\url", "")
        text = text.replace("preparationtime", "Vorbereitungszeit")
        text = text.replace("portion", "Portion")
        text = text.replace("calory", "Kalorien")
        text = text.replace("source", "Quelle")
        return text.strip()


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input folder holding xcookybooky files.")
    parser.add_argument("-o", help="Output folder ~/something/pages.")
    args = parser.parse_args()

    folderIn = None
    if args.t:
        fileIn = args.i
    else:
        print('No input file given.')
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
