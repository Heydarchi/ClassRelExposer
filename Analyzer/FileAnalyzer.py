import re
from AbstractAnalyzer import * 
from ClassAnalyzer import *
from ClassUmlDrawer import *
from PythonUtilityClasses import SystemUtility as SU
class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        if not os.path.exists("../out"):
            os.makedirs("../out")

    def analyze(self, targetPath, pattern):
        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.getListOfFiles(targetPath, "*")
        print(listOfFiles)
        for filePath in listOfFiles:
            classAnalyzer = ClassAnalyzer()
            language = self.detectLang(filePath)
            print(filePath,": ", language)
            if language != FileTypeEnum.UNDEFINED :
                listOfClasses = classAnalyzer.analyze(filePath, language)
                self.drawUmls(listOfClasses)

    def drawUmls(self, listOfClassNodes):
        for classInfo in listOfClassNodes:
            umlDrawer = ClassUmlDrawer()
            umlDrawer.drawUml(classInfo)

    def detectLang(self, fileName):
        if ".java" in fileName:
            return FileTypeEnum.JAVA
        elif ".cpp" in fileName:
            return FileTypeEnum.CPP
        else:
            return FileTypeEnum.UNDEFINED
        
        

if __name__ == "__main__" :
    print(sys.argv)
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyze(sys.argv[1], None)