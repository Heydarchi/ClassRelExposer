from dataclasses import dataclass
from typing import List


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

@dataclass
class ClassNode:
    name: str
    dataType: str
    accessLevel: str
    isStatic: bool
    isFinal: bool
    variables: List[VariableNode]
    methods: List[MethodNode]