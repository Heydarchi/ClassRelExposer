import sys
from pathlib import Path

import re
from AbstractAnalyzer import * 
from PythonUtilityClasses import FileReader as FR
class VariableAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.replaceByStr = dict()
        self.initPatterns()

    def initPatterns(self):
        self.pattern["cpp"]=("[\\s;\\n{}(::)]([a-zA-Z0-9_<>])+\\s+(\\*)?\\s?[a-zA-Z_,<>][a-zA-Z0-9_,<>]*\\s?[\\r\\n]?[;=]")
        self.pattern["java"]=("[\\s;\\n{}}][(public|private)\\s+|(static)\\s+|(final)\\s+].*(([a-zA-Z0-9_<>])+::)?([a-zA-Z0-9_<>])+\\s+(\\*)?\\s?[a-zA-Z_,<>][a-zA-Z0-9_,<>]*\\s?[\\r\\n]?[;=]")


    def analyze(self, filePath, lang):
        fileReader = FR.FileReader()
        fileContent= fileReader.readFile(filePath)
        tempContent = fileContent
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
    vriableAnalyzer.analyze(sys.argv[1], "java")

