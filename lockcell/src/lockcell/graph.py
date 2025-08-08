from typing import List, Tuple, Optional


## Generate unique graph id
class IdGen:
    """
    An ID generator to uniquely identify each node.

    # TODO: Not supported on ArmoniK yet, since each parallel task would generate IDs independently.
    # A possible workaround is to generate collision-free IDs by concatenating a task-specific prefix
    # (e.g., worker ID) with a local counter.
    """

    def __init__(self) -> None:
        self.count = -1

    def Gen(self):
        self.count += 1
        return self.count


gen = IdGen()

### GRAPH ###########################################################################


class Node:
    """
    Represents a node and its connections in the task graph.

    Each node can have:
    - upstream connections (`up`)
    - downstream connections (`son`)
    - an output (`out`)

    Attributes:
        type (str): A label representing the node type or description.
        id (str): A unique identifier for the node (generated via `gen.Gen()`).
        son (List[Tuple[Node, Tuple[list, bool], str]]): List of downstream nodes,
            with associated data and an optional label.
        up (list): List of upstream connections in the form `(Node, data)`.
        emphasis (str): The color used to highlight this node in a graph representation.
        out (Tuple[Node, Tuple[list, bool] | None]): Output connection and its data.
    """

    def __init__(self, obj=None, emphas: Optional[str] = None):
        """
        Initialize a new Node.

        Args:
            obj (optional): Initial upstream connections (`up`) to set for this node.
            emphas (Optional[str]): Color for node emphasis (default: "black").
        """
        self.type = "ERR"
        self.id = gen.Gen().__str__()
        self.son: List[Tuple[Node, Tuple[list, bool], str]] = []
        self.up = []
        self.emphasis = "black"
        if emphas is not None:
            self.emphasis = emphas
        if obj is not None:
            self.up = obj
        self.out: Tuple[Node, Tuple[list, bool]] = (self, None)  # type: ignore

    def setType(self, type: str):
        """
        Set the type (label) of the node.

        Args:
            type (str): New type label for this node.
        """
        self.type = type

    def addLabel(self, label: str):
        """
        Append a label to the node's type.

        Args:
            label (str): Additional label text.
        """
        self.type += "\n" + label

    def sup(self, obj, data):
        """
        Add an upstream connection.

        Args:
            obj (Node): The upstream node.
            data (Any): Associated data for this connection.
        """
        self.up.append((obj, data))

    def down(self, obj, data, label=""):
        """
        Add a downstream connection.

        Args:
            obj (Node): The downstream node.
            data (Any): Associated data for this connection.
            label (str, optional): Label describing this connection.
        """
        self.son.append((obj, data, label))

    def sout(self, obj, data):
        """
        Set the node's output connection.

        Args:
            obj (Node): The output node.
            data (Any): Associated data for the output.
        """
        self.out = (obj, data)

    def setEmphasis(self, color: str):
        """
        Change the emphasis color of the node.

        Args:
            color (str): New color for emphasis.
        """
        self.emphasis = color

    def __repr__(self) -> str:
        """
        Return a string representation of the node.

        Returns:
            str: A string with the node's ID.
        """
        return f"Node : {self.id}"
