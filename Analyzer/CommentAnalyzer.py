import sys
from pathlib import Path

import re
from AbstractAnalyzer import * 
from PythonUtilityClasses import FileReader as FR
class CommentAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.replaceByStr = dict()
        self.initPatterns()

    def initPatterns(self):
        self.pattern["cpp"]=["(\\/\\/).*", "(\\/\\*).*([a-zA-Z0-9\\s]*|\\r|\\n).*(\\*\\/)", "(\\\").*[\\r\\na-zA-Z0-9\\s].*(\\\")"]
        self.pattern["java"]=["(\\/\\/).*", "(\\/\\*).*([a-zA-Z0-9\\s]*|\\r|\\n).*(\\*\\/)", "(\\\").*[\\r\\na-zA-Z0-9\\s].*(\\\")"]

        self.replaceByStr["cpp"]=["//@", "/*@*/", "\"@\""]
        self.replaceByStr["java"]=["//@", "/*@*/", "\"@\""]

    def analyze(self, filePath, lang):
        fileReader = FileReader()
        fileContent= fileReader.readFile(filePath)
        print( str(fileContent).rstrip()) 
        for pattern in self.pattern[lang]:
            #regxFinder=re.compile(pattern)

            print(pattern)
            x = re.findall(pattern, str(fileContent))
            print ("regx: ", x)
'''           match = re.search(pattern, str(fileContent))
            while match != None: 
                print("\n-------Match at index % s, % s" % (match.start(), match.end()),str(fileContent)[match.start():match.end()])
                match = re.search(pattern, str(fileContent)[match.end():])
'''
if __name__ == "__main__" :
    print(sys.argv)
    #commentAnalyzer = CommentAnalyzer()
    #commentAnalyzer.analyze(sys.argv[1], "cpp")
    fileReader = FR.FileReader()
    fileContent= fileReader.readFile(sys.argv[1])
    print(fileContent)
