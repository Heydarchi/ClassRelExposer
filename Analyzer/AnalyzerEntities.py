from dataclasses import dataclass, field
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

class AccessEnum(Enum):
    PUBLIC = 1
    PRIVATE = 2
    PROTECTED = 3

@dataclass
class Inheritance:
    name: str 
    relationship: InheritanceEnum    

@dataclass
class ClassNode:
    name: str = ""
    accessLevel: AccessEnum = AccessEnum.PUBLIC 
    isStatic: bool = False
    isFinal: bool = False
    isInterface: bool = False
    variables: List[VariableNode] = field(default_factory=list)
    methods: List[MethodNode] = field(default_factory=list)
    relations: List[Inheritance] = field(default_factory=list)