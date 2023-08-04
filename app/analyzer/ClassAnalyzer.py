import sys
import re
from analyzer.AbstractAnalyzer import *
from analyzer.MethodAnalyzer import *
from analyzer.VariableAnalyzer import *
from analyzer.AnalyzerHelper import *
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
        self.pattern[
            FileTypeEnum.CPP
        ] = "(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?(class)\\s+[a-zA-Z0-9_\\s]*[:{;]"
        self.pattern[FileTypeEnum.JAVA] = [
            "(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?[(public|private)\\s+|(static)\\s+|(final)\\s+].*((class|interface|implements|extends)\\s+[a-zA-Z0-9_\\s]*)+[:{;]"
        ]
        self.pattern[FileTypeEnum.CSHARP] = [
            "(\\;|\\{|\\})*(\\r|\\n)*\\s*(\\r|\\n)*(\\/\\/\\s?[a-zA-Z0-9_].*(\\r|\\n)?)?(\\r|\\n)?\\s?[(public|private)\\s+|(static)\\s+|(final)\\s+].*((class|interface)\\s+)[a-zA-Z0-9_]+\\s?(:)?\\s?(\\n)?[a-zA-Z0-9_\\s]*(\\n)?[{;](\\n)?"
        ]

        self.classNamePattern[FileTypeEnum.CPP] = "(class)\\s+([a-zA-Z0-9_])*\\s+"
        self.classNamePattern[
            FileTypeEnum.JAVA
        ] = "(class|interface)\\s+([a-zA-Z0-9_])+\\s+"
        self.classNamePattern[
            FileTypeEnum.CSHARP
        ] = "(class|interface)\\s+([a-zA-Z0-9_])+\\s?"

        self.classImplementPattern[FileTypeEnum.CPP] = "(class)\\s+([a-zA-Z0-9_])*\\s+"
        self.classImplementPattern[
            FileTypeEnum.JAVA
        ] = "(implements)\\s+([a-zA-Z0-9_])+[:{;\\r\\n\\s]"
        self.classImplementPattern[
            FileTypeEnum.CSHARP
        ] = "(:)\\s?(\\n)?[a-zA-Z0-9_\s]+\\s?\\n?\\s?[; {]"

        self.classExtendPattern[FileTypeEnum.CPP] = "(class)\\s+([a-zA-Z0-9_])*\\s+"
        self.classExtendPattern[
            FileTypeEnum.JAVA
        ] = "(extends)\\s+([a-zA-Z0-9_])+[:{;\\r\\n\\s]"
        self.classExtendPattern[
            FileTypeEnum.CSHARP
        ] = "(:)\\s?(\\n)?[a-zA-Z0-9_\s]+\\s?\\n?\\s?[; {]"

    def analyze(self, filePath, lang, inputStr=None):
        if inputStr == None:
            fileReader = FR.FileReader()
            fileContent = fileReader.read_file(filePath)
        else:
            fileContent = inputStr

        print("\n********************\n", str(fileContent).rstrip())
        listOfClasses = list()
        for pattern in self.pattern[lang]:
            tempContent = fileContent
            # print ("\nregx: ", pattern)
            match = re.search(pattern, tempContent)
            while match != None:
                classInfo = ClassNode()
                print(
                    "-------Match at begin % s, end % s "
                    % (match.start(), match.end()),
                    tempContent[match.start(): match.end()],
                )
                classInfo.name = self.extractClassName(
                    lang, tempContent[match.start(): match.end()]
                )
                # print("====> Class/Interface name: ",classInfo.name)
                classInfo.relations = self.extractClassInheritances(
                    lang, tempContent[match.start(): match.end()]
                )
                # print("====> classInfo.relations: ", classInfo.relations)
                classInfo = self.extractClassSpec(
                    tempContent[match.start(): match.end()], classInfo
                )

                classBoundary = AnalyzerHelper().findClassBoundary(
                    lang, tempContent[match.start():]
                )

                """### Find the variables & methods before the class's begin
                methods = MethodAnalyzer().analyze(None , lang, tempContent[:match.start())] )
                classInfo.methods.extend(methods)

                variables = VariableAnalyzer().analyze(None , lang, tempContent[:match.start()] )
                classInfo.variables.extend(variables)
                """

                ### Find the variables & methods within the class's boundary
                methods = MethodAnalyzer().analyze(
                    None,
                    lang,
                    tempContent[match.start(): (match.end() + classBoundary)],
                )
                classInfo.methods.extend(methods)

                variables = VariableAnalyzer().analyze(
                    None,
                    lang,
                    tempContent[match.start(): (match.end() + classBoundary)],
                )
                classInfo.variables.extend(variables)

                classAnalyzer = ClassAnalyzer()
                classInfo.classes = classAnalyzer.analyze(
                    None,
                    lang,
                    inputStr=tempContent[match.end(): (match.end() + classBoundary)],
                )

                listOfClasses.append(classInfo)

                tempContent = tempContent[match.end() + classBoundary:]
                match = re.search(pattern, tempContent)
        # print (listOfClasses)
        return listOfClasses

    def extractClassName(self, lang, inputStr):
        print("++++++++++++ extractClassName:   ", inputStr)
        match = re.search(self.classNamePattern[lang], inputStr)
        if match != None:
            className = inputStr[match.start(): match.end()].strip().split(" ")[1]
            return className
        else:
            return None

    def extractClassInheritances(self, lang, inputStr):
        inheritance = list()
        match = re.search(self.classExtendPattern[lang], inputStr)
        if match != None:
            # print("classExtendName: ", " ".join(inputStr[match.start():match.end()].replace("\n"," ").split()).strip())
            inherit = Inheritance(
                name=" ".join(
                    inputStr[match.start(): match.end()].replace("\n", " ").split()
                )
                .strip()
                .split(" ")[1],
                relationship=InheritanceEnum.EXTENDED,
            )
            inheritance.append(inherit)

        classImplementName = None
        match = re.search(self.classImplementPattern[lang], inputStr)
        if match != None and lang == FileTypeEnum.JAVA:
            # print("classImplementName: ", " ".join(inputStr[match.start():match.end()].replace("\n"," ").split()).strip())
            inherit = Inheritance(
                name=" ".join(
                    inputStr[match.start(): match.end()].replace("\n", " ").split()
                )
                .strip()
                .split(" ")[1],
                relationship=InheritanceEnum.IMPLEMENTED,
            )
            inheritance.append(inherit)

        return inheritance

    def extractClassSpec(self, inputStr: str, classInfo: ClassNode):
        splittedStr = inputStr.split()
        if "public" in splittedStr:
            classInfo.accessLevel = AccessEnum.PUBLIC
        elif "protected" in splittedStr:
            classInfo.accessLevel = AccessEnum.PROTECTED
        else:
            classInfo.accessLevel = AccessEnum.PRIVATE

        if "final" in splittedStr:
            classInfo.isFinal = True

        if "interface" in splittedStr:
            classInfo.isInterface = True

        return classInfo


if __name__ == "__main__":
    print(sys.argv)
    classAnalyzer = ClassAnalyzer()
    classAnalyzer.analyze(sys.argv[1], FileTypeEnum.JAVA)
