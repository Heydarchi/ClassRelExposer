import os, sys
from model.AnalyzerEntities import *
from model.DataGeneratorEntities import *

from PythonUtilityClasses import FileWriter as FW
from datetime import datetime


class DataGenerator:
    def __init__(self) -> None:
        self.graphData = GraphData()
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

    def generateData(self, listOfClassNodes: ClassNode):
        dataList = list()

        # print(listOfClassNodes)

        for node in listOfClassNodes:

            self.dumpClass(node)

        # print("\n\n")
        # print(self.graphData)
        json_output = self.graphData.to_json()

        date_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

        filePath = "static/out/data" + date_time + ".json"
        self.writeToFile(filePath, json_output)

    def dumpClass(self, classInfo: ClassNode):
        classData = ClassData()
        classData.package = classInfo.package
        classData.id = classInfo.name

        # Convert methods explicitly (currently empty, but future-proof)
        classData.methods = [
            method.name if hasattr(method, "name") else str(method)
            for method in classInfo.methods
        ]

        # Explicitly handle attributes (variables)
        classData.attributes = [
            f"{var.accessLevel.name.lower()} {var.dataType} {var.name}".replace(
                ";", ""
            ).strip()
            for var in classInfo.variables
            if var.dataType not in self.dataTypeToIgnore
        ]

        self.graphData.nodes.append(classData)

        # Handle relationships explicitly
        for relation in classInfo.relations:
            dependency = Dependency()
            dependency.source = classInfo.name
            dependency.target = self.fix_name_issue(relation.name)
            dependency.relation = (
                relation.relationship.name.lower()
            )  # Clearly specify relationship type
            self.graphData.links.append(dependency)

    def writeToFile(self, fileName, json_output):
        with open(fileName, "w") as f:
            f.write(json_output)

    def fix_name_issue(self, name):
        if ">" in name or "<" in name:
            return '"' + name + '"'
        return name


if __name__ == "__main__":
    print(sys.argv)
    classInfo = ClassNode()
    classInfo.name = "TestClass"
    classInfo.relations.append(Inheritance("Class1", InheritanceEnum.DEPENDED))
    classInfo.relations.append(Inheritance("Class2", InheritanceEnum.EXTENDED))
    classInfo.relations.append(Inheritance("Class3", InheritanceEnum.IMPLEMENTED))
    classUmlDrawer = ClassUmlDrawer()
    classUmlDrawer.drawUml(classInfo)
