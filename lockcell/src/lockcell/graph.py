from typing import List, Tuple, Optional


## Generate unique graph id
class IdGen:
    def __init__(self) -> None:
        self.count = -1

    def Gen(self):
        self.count += 1
        return self.count


gen = IdGen()

### GRAPH ###########################################################################


class Graph:
    def __init__(self, obj=None, emphas: Optional[str] = None):
        self.type = "ERR"
        self.id = gen.Gen().__str__()
        self.son: List[Tuple[Graph, Tuple[list, bool], str]] = []
        self.up = []
        self.emphasis = "black"
        if emphas is not None:
            self.emphasis = emphas
        if obj is not None:
            self.up = obj
        self.out: Tuple[Graph, Tuple[list, bool]] = (self, None)  # type: ignore

    def setType(self, type: str):
        self.type = type

    def addLabel(self, label: str):
        self.type += "\n" + label

    def sup(self, obj, data):
        self.up.append((obj, data))

    def down(self, obj, data, label=""):
        self.son.append((obj, data, label))

    def sout(self, obj, data):
        self.out = (obj, data)

    def setEmphasis(self, color: str):
        self.emphasis = color

    def __repr__(self) -> str:
        return f"Graph : {self.id}"
