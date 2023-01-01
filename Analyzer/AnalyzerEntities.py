from dataclasses import dataclass
from typing import List
from enum import Enum

@dataclass
class VariableNode:
    name: str
    dataType: str
    accessLevel: str
    isStatic: bool

@dataclass
class MethodNode:
    name: str
    dataType: str
    accessLevel: str
    isStatic: bool

class InheritanceEnum(Enum):
    EXTENDED = 1
    IMPLEMENTED = 2
    DEPENDED = 3

@dataclass
class Inheritance:
    name: str
    relationship: InheritanceEnum    

@dataclass

@dataclass
class ClassNode:
    name: str
    dataType: str
    accessLevel: str
    isStatic: bool
    isFinal: bool
    isInterface: bool
    variables: List[VariableNode]
    methods: List[MethodNode]
    relations: List[Inheritance]