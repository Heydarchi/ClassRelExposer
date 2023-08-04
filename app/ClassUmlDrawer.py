import os, sys
from AnalyzerEntities import *
from PythonUtilityClasses import FileWriter as FW


class ClassUmlDrawer:
    def __init__(self) -> None:
        self.mapList = list()
        self.mapList.append(UmlRelationMap("", InheritanceEnum.DEPENDED))
        self.mapList.append(UmlRelationMap("", InheritanceEnum.EXTENDED))
        self.mapList.append(UmlRelationMap("", InheritanceEnum.IMPLEMENTED))

        self.dataTypeToIgnore = [
            "boolean",
            "byte",
            "char",
            "short",
            "int",
            "long",
            "float",
            "double",
            "void",
            "Int",
            "return",
            "var",
        ]

    def drawUml(self, classInfo: ClassNode):
        plantUmlList = list()
        plantUmlList.append("@startuml")

        """
        if classInfo.isInterface:
            plantUmlList.append("interface " + classInfo.name)
        else:
            plantUmlList.append("class " + classInfo.name)
        """
        plantUmlList.extend(self.dumpClass(classInfo))

        plantUmlList.append("@enduml")

        # Remove redundance items
        plantUmlList = list(dict.fromkeys(plantUmlList))

        filePath = "../out/" + classInfo.name + "_uml.puml"
        self.writeToFile(filePath, plantUmlList)
        self.generatePng(filePath)
        print(classInfo)

    def dumpClass(self, classInfo: ClassNode):
        plantUmlList = list()

        for relation in classInfo.relations:
            if relation.relationship == InheritanceEnum.DEPENDED:
                plantUmlList.append(classInfo.name + " .....> " + relation.name)
            if relation.relationship == InheritanceEnum.IMPLEMENTED:
                plantUmlList.append(classInfo.name + " .....> " + relation.name)
            if relation.relationship == InheritanceEnum.EXTENDED:
                plantUmlList.append(classInfo.name + " -----|> " + relation.name)

        for innerClass in classInfo.classes:
            plantUmlList.extend(self.dumpClass(innerClass))
        plantUmlList.extend(self.drawVariables(classInfo.name, classInfo.variables))
        plantUmlList.extend(self.drawMethods(classInfo.name, classInfo.methods))
        return plantUmlList

    def drawClasses(self, className, listOfClasses):
        classsUml = list()
        for _class in listOfClasses:
            classsUml.append(className + " .....> " + _class.name)
        return classsUml

    def drawMethods(self, className, listOfMethods):
        methodUml = list()
        for method in listOfMethods:
            if method.dataType != None:
                methodUml.append(className + " .....> " + method.dataType)
            methodUml.extend(self.drawVariables(className, method.variables))
        return methodUml

    def drawVariables(self, className, listOfVariables):
        variableUml = list()
        for variable in listOfVariables:
            if variable.dataType not in self.dataTypeToIgnore:
                variableUml.append(className + " .....> " + variable.dataType)
        return variableUml

    def generatePng(self, filepath):
        os.system("java -jar plantuml/plantuml.jar " + filepath)

    def writeToFile(self, fileName, listOfStr):
        fw = FW.FileWriter()
        fw.writeListToFile(fileName, listOfStr)


if __name__ == "__main__":
    print(sys.argv)
    classInfo = ClassNode()
    classInfo.name = "TestClass"
    classInfo.relations.append(Inheritance("Class1", InheritanceEnum.DEPENDED))
    classInfo.relations.append(Inheritance("Class2", InheritanceEnum.EXTENDED))
    classInfo.relations.append(Inheritance("Class3", InheritanceEnum.IMPLEMENTED))
    classUmlDrawer = ClassUmlDrawer()
    classUmlDrawer.drawUml(classInfo)
