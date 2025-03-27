import os, sys
from model.AnalyzerEntities import *
from PythonUtilityClasses import FileWriter as FW

import json
from typing import List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ClassData:
    id: str = ""
    type: str = "class"
    attributes: Optional[List[str]] = field(default_factory=list)
    methods: Optional[List[str]] = field(default_factory=list)
    linesOfCode: Optional[int] = None
    complexity: Optional[str] = None
    module: Optional[str] = None


@dataclass
class ModuleData:
    id: str = ""
    type: str = "module"
    version: Optional[str] = None
    linesOfCode: Optional[int] = None
    classes: Optional[List[str]] = field(default_factory=list)


@dataclass
class Dependency:
    source: str = ""
    target: str = ""
    relation: str = ""


from dataclasses import dataclass, field, asdict
from typing import List
import json


@dataclass
class GraphData:
    nodes: List = field(default_factory=list)
    links: List = field(default_factory=list)

    def add_blank_classes(self):
        defined_nodes = {node.id for node in self.nodes}
        referenced_nodes = {link.source for link in self.links}.union(
            {link.target for link in self.links}
        )

        undefined_nodes = referenced_nodes - defined_nodes

        for undefined_node in undefined_nodes:
            blank_node = ClassData(
                id=undefined_node,
                attributes=[],
                methods=[],
                linesOfCode=None,
                complexity=None,
                module=None,
            )
            self.nodes.append(blank_node)

    def remove_duplicates(self):
        # Remove duplicate nodes explicitly based on 'id'
        unique_nodes = {}
        for node in self.nodes:
            node_id = node.id
            if node_id not in unique_nodes:
                unique_nodes[node_id] = node
        self.nodes = list(unique_nodes.values())

        # Remove duplicate links explicitly based on 'source', 'target', 'relation'
        unique_links = set()
        filtered_links = []
        for link in self.links:
            link_id = (link.source, link.target, link.relation)
            if link_id not in unique_links:
                unique_links.add(link_id)
                filtered_links.append(link)
        self.links = filtered_links

    def to_json(self) -> str:
        # Ensure duplicates are explicitly removed before converting to JSON
        self.remove_duplicates()
        self.add_blank_classes()
        return json.dumps(asdict(self), indent=4)


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

        print(listOfClassNodes)

        for node in listOfClassNodes:

            self.dumpClass(node)

        # print("\n\n")
        # print(self.graphData)
        json_output = self.graphData.to_json()

        filePath = "static/out/data.json"
        self.writeToFile(filePath, json_output)

    def dumpClass(self, classInfo: ClassNode):
        classData = ClassData()
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
