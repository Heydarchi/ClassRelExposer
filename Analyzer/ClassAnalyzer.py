import sys
import re
from AbstractAnalyzer import * 
from AnalyzerEntities import *
from PythonUtilityClasses import FileReader as FR
class ClassAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        self.pattern = dict()
        self.classNamePattern = dict()
        self.classInheritancePattern = dict()
        self.classImplementPattern = dict()
        self.classExtendPattern = dict()
        self.initPatterns()

    def initPatterns(self):
        self.pattern[FileTypeEnum.CPP]=("(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?(class)\\s+[a-zA-Z0-9_\\s]*[:{;]")
        self.pattern[FileTypeEnum.JAVA]=["(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?[(public|private)\\s+|(static)\\s+|(final)\\s+].*((class|interface|implements|extends)\\s+[a-zA-Z0-9_\\s]*)+[:{;]"]

        self.classNamePattern[FileTypeEnum.CPP]=("(class)\\s+([a-zA-Z0-9_])*\\s+")
        self.classNamePattern[FileTypeEnum.JAVA]=("(class|interface)\\s+([a-zA-Z0-9_])+\\s+")

        self.classImplementPattern[FileTypeEnum.CPP]=("(class)\\s+([a-zA-Z0-9_])*\\s+")
        self.classImplementPattern[FileTypeEnum.JAVA]=("(implements)\\s+([a-zA-Z0-9_])+[:{;\\r\\n\\s]")

        self.classExtendPattern[FileTypeEnum.CPP]=("(class)\\s+([a-zA-Z0-9_])*\\s+")
        self.classExtendPattern[FileTypeEnum.JAVA]=("(extends)\\s+([a-zA-Z0-9_])+[:{;\\r\\n\\s]")


    def analyze(self, filePath, lang):
        fileReader = FR.FileReader()
        fileContent= fileReader.readFile(filePath)
        #print( str(fileContent).rstrip()) 
        listOfClasses = list()
        for pattern in self.pattern[lang]:
            tempContent = fileContent
            #print ("\nregx: ", pattern)
            match = re.search(pattern, tempContent)
            while match != None: 
                classInfo = ClassNode()
                print("-------Match at begin % s, end % s " % (match.start(), match.end()),tempContent[match.start():match.end()])
                classInfo.name = self.extractClassName(lang, tempContent[match.start():match.end()])
                print("====> Class/Interface name: ",classInfo.name)
                classInfo.relations = self.extractClassInheritances(lang, tempContent[match.start():match.end()])
                print("====> classInfo.relations: ", classInfo.relations)
                classInfo = self.extractClassSpec(tempContent[match.start():match.end()], classInfo)
                listOfClasses.append( classInfo )
                tempContent = tempContent[match.end():]
                match = re.search(pattern, tempContent)
        print (listOfClasses)
        return listOfClasses 

    def extractClassName(self, lang, inputStr):
            match = re.search(self.classNamePattern[lang], inputStr)
            if match != None: 
                className = inputStr[match.start():match.end()].strip().split(" ")[1]
                return className
            else:
                return None

    def extractClassInheritances(self, lang, inputStr):
            inheritance = list()
            match = re.search(self.classExtendPattern[lang], inputStr)
            if match != None:
                #print("classExtendName: ", " ".join(inputStr[match.start():match.end()].replace("\n"," ").split()).strip())
                inherit = Inheritance(name = " ".join(inputStr[match.start():match.end()].replace("\n"," ").split()).strip().split(" ")[1],
                    relationship = InheritanceEnum.EXTENDED)
                inheritance.append(inherit) 

            classImplementName = None
            match = re.search(self.classImplementPattern[lang], inputStr)
            if match != None: 
                #print("classImplementName: ", " ".join(inputStr[match.start():match.end()].replace("\n"," ").split()).strip())
                inherit = Inheritance(name = " ".join(inputStr[match.start():match.end()].replace("\n"," ").split()).strip().split(" ")[1],
                    relationship = InheritanceEnum.IMPLEMENTED)
                inheritance.append(inherit)

            return inheritance


    def extractClassSpec(self, inputStr: str, classInfo: ClassNode):
        splittedStr = inputStr.split()
        if "privat" in splittedStr :
            classInfo.accessLevel = AccessEnum.PRIVATE
        elif "protected" in splittedStr:
            classInfo.accessLevel = AccessEnum.PROTECTED
        else:
            classInfo.accessLevel = AccessEnum.PUBLIC

        if "final" in splittedStr:
            classInfo.isFinal = True
                    
        if "interface" in splittedStr:
            classInfo.isInterface = True

        return classInfo

if __name__ == "__main__" :
    print(sys.argv)
    classAnalyzer = ClassAnalyzer()
    classAnalyzer.analyze(sys.argv[1], FileTypeEnum.JAVA)