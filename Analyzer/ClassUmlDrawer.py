import os, sys
from AnalyzerEntities import  *
from PythonUtilityClasses import FileWriter as FW
class ClassUmlDrawer:

    def __init__(self) -> None:
        self.mapList = list()
        self.mapList.append( UmlRelationMap("", InheritanceEnum.DEPENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.EXTENDED))
        self.mapList.append( UmlRelationMap("", InheritanceEnum.IMPLEMENTED))

    def drawUml(self, classInfo: ClassNode):
        plantUmlList = list()
        plantUmlList.append("@startuml")
        '''
        if classInfo.isInterface:
            plantUmlList.append("interface " + classInfo.name)
        else:
            plantUmlList.append("class " + classInfo.name)
        '''
        for relation in classInfo.relations:
            if relation.relationship == InheritanceEnum.DEPENDED:
                plantUmlList.append(classInfo.name + " .....> " + relation.name)
            if relation.relationship == InheritanceEnum.IMPLEMENTED:
                plantUmlList.append(classInfo.name + " .....> " + relation.name)
            if relation.relationship == InheritanceEnum.EXTENDED:
                plantUmlList.append(classInfo.name + " -----|> " + relation.name)

        plantUmlList.extend(self.drawVariables(classInfo.name, classInfo.variables))
        plantUmlList.extend(self.drawMethods(classInfo.name, classInfo.methods))

        plantUmlList.append("@enduml")
        self.writeToFile(classInfo.name+"_uml.puml", plantUmlList)

    def drawMethods(self, className, listOfMethods):
        methodUml = list()
        for method in listOfMethods:
                methodUml.extend(self.drawVariables(className, method.variables))
        return methodUml

    def drawVariables(self, className, listOfVariables):
        variableUml = list()
        for variable in listOfVariables:
                variableUml.append(className + " .....> " + variable.dataType)
        return variableUml

    def writeToFile(self, fileName, listOfStr):
        fw = FW.FileWriter()
        fw.writeListToFile(fileName, listOfStr)

if __name__ == "__main__" :
    print(sys.argv)
    classInfo = ClassNode()
    classInfo.name = "TestClass"
    classInfo.relations.append( Inheritance("Class1", InheritanceEnum.DEPENDED) )
    classInfo.relations.append( Inheritance("Class2", InheritanceEnum.EXTENDED) )
    classInfo.relations.append( Inheritance("Class3", InheritanceEnum.IMPLEMENTED) )
    classUmlDrawer = ClassUmlDrawer()
    classUmlDrawer.drawUml(classInfo)