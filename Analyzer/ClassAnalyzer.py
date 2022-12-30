import sys
import re
from AbstractAnalyzer import * 
from PythonUtilityClasses import FileReader as FR

class ClassAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.classNamePattern = dict()
        self.classInheritancePattern = dict()
        self.initPatterns()

    def initPatterns(self):
        self.pattern["cpp"]=("(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?(class)\\s+[a-zA-Z0-9_\\s]*[:{;]")
        self.pattern["java"]=["(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?(public|private)?\\s+(static)?\\s?((class|interface|implements)\\s+[a-zA-Z0-9_\\s]*)+[:{;]"]

        self.classNamePattern["cpp"]=("(class)\\s+([a-zA-Z0-9_])*\\s+")
        self.classNamePattern["java"]=("(class|interface)\\s+([a-zA-Z0-9_])*\\s+")

        self.classInheritancePattern["cpp"]=("(class)\\s+([a-zA-Z0-9_])*\\s+")
        self.classInheritancePattern["java"]=("(class|interface)\\s+([a-zA-Z0-9_])*\\s+")

    def analyze(self, filePath, lang):
        fileReader = FR.FileReader()
        fileContent= fileReader.readFile(filePath)
        #print( str(fileContent).rstrip()) 
        for pattern in self.pattern[lang]:
            tempContent = fileContent
            #print ("\nregx: ", pattern)
            match = re.search(pattern, tempContent)
            while match != None: 
                #print("-------Match at begin % s, end % s " % (match.start(), match.end()),tempContent[match.start():match.end()])
                className = self.extractClassName(lang, tempContent[match.start():match.end()])
                print("====> Class/Interface name: ",className)
                tempContent = tempContent[match.end():]
                match = re.search(pattern, tempContent)

    def extractClassName(self, lang, inputStr):
            match = re.search(self.classNamePattern[lang], inputStr)
            if match != None: 
                className = inputStr[match.start():match.end()].strip().split(" ")[1]
                return className
            else:
                return None

    def extractClassInheritances(self):
        pass


if __name__ == "__main__" :
    print(sys.argv)
    classAnalyzer = ClassAnalyzer()
    classAnalyzer.analyze(sys.argv[1], "java")