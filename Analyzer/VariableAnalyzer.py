import sys
from pathlib import Path

import re
from AbstractAnalyzer import * 
from AnalyzerEntities import *
from PythonUtilityClasses import FileReader as FR
class VariableAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.replaceByStr = dict()
        self.initPatterns()

    def initPatterns(self):
        self.pattern[FileTypeEnum.CPP]=("[\\s;\\n{}(::)]([a-zA-Z0-9_<>])+\\s+(\\*)?\\s?[a-zA-Z_,<>][a-zA-Z0-9_,<>]*\\s?[\\r\\n]?[;=]")
        self.pattern[FileTypeEnum.JAVA]=("[\\s;\\n{}}][(public|private)\\s+|(static)\\s+|(final)\\s+].*(([a-zA-Z0-9_<>])+::)?([a-zA-Z0-9_<>])+\\s+(\\*)?\\s?[a-zA-Z_,<>][a-zA-Z0-9_,<>]*\\s?[\\r\\n]?[;=]")


    def analyze(self, filePath, lang, classStr = None):
        listOfvariables = list()
        if classStr == None:
            fileReader = FR.FileReader()
            tempContent= fileReader.readFile(filePath)
        else:
            tempContent = classStr

        print ("\nregx: ", self.pattern[lang])
        match = re.search(self.pattern[lang], tempContent)
        #if match != None: 
        #    print("\n-------Match at index % s, % s" % (match.start(), match.end()),str(fileContent)[match.start():match.end()])
        while match != None: 
            print("-------Match at begin % s, end % s " % (match.start(), match.end()),tempContent[match.start():match.end()])
            tempContent = tempContent[match.end():]
            match = re.search(self.pattern[lang], tempContent)

if __name__ == "__main__" :
    print(sys.argv)
    vriableAnalyzer = VariableAnalyzer()
    vriableAnalyzer.analyze(sys.argv[1], FileTypeEnum.JAVA)

