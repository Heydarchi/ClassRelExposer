from analyzer.ClassAnalyzer import *
from PythonUtilityClasses import SystemUtility as SU
from drawer.DataGenerator import *


class FileAnalyzer(AbstractAnalyzer):
    def __init__(self) -> None:
        if not os.path.exists("static/out"):
            os.makedirs("static/out")

    def analyze(self, targetPath, pattern):
        systemUtility = SU.SystemUtility()
        listOfFiles = systemUtility.get_list_of_files(targetPath, "*")
        print(listOfFiles)
        listOfClassNodes = list()
        for filePath in listOfFiles:
            classAnalyzer = ClassAnalyzer()
            language = self.detectLang(filePath)
            if language != FileTypeEnum.UNDEFINED:
                print("- Analyzing: " + filePath, language)
                listOfClasses = classAnalyzer.analyze(filePath, language)
                listOfClassNodes.extend(listOfClasses)
            else:
                #print("- Undefined file extension : " + filePath)
                pass
        self.generateData(listOfClassNodes)

    def generateData(self, listOfClassNodes):
        dataGenerator = DataGenerator()
        dataGenerator.generateData(listOfClassNodes)

    def detectLang(self, fileName):
        if ".java" in fileName:
            return FileTypeEnum.JAVA
        elif ".cpp" in fileName or ".h" in fileName:
            return FileTypeEnum.CPP
        elif ".cs" in fileName:
            return FileTypeEnum.CSHARP
        elif ".kt" in fileName:
            return FileTypeEnum.KOTLIN
        else:
            return FileTypeEnum.UNDEFINED


if __name__ == "__main__":
    print(sys.argv)
    fileAnalyzer = FileAnalyzer()
    fileAnalyzer.analyze(sys.argv[1], None)
