"""
Created on : 2025-07-17
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""

### AFFICHAGE DU GRAPHE DES TÂCHES

from graphviz import Digraph
from .graph import Node
from typing import List, Optional


class MultiViz:
    """
    Handles the printing of many graphs.

    Attributes:
       active (bool): If False, doesn't generates anything and return None instead of new Graphs.
                   Defaults to False.
       graphs (List[VizPrint]): A list of graphs
    """

    def __init__(self, active: bool = False):
        """
        __init__ Initialize the MultiViz

        Args:
            active (bool, optional): If False, doesn't generates anything and return None instead of new Graphs.
                    Defaults to False.
        """
        self.active: bool = active
        self.graphs: List[VizPrint] = []

    def newGraph(self, fake=False) -> Optional[Node]:
        """
        newGraph Creates a new Graph and returns it if active

        Args:
            fake (bool, optional): if True returns None. Defaults to False.

        Returns:
            Optional[Node]: The root of the Graph
        """
        if fake:
            return None
        self.graphs.append(VizPrint())
        return self.graphs[-1].getGraph(self.active)

    def aff(self, i: int):
        """
        aff print graphs

        Args:
            i (int): which graph to print
        """
        self.graphs[i].aff(i)

    def __len__(self):
        return len(self.graphs)

    def aff_all(self):
        """
        aff_all Print all graphs contained
        """
        i = 0
        for graph in self.graphs:
            graph.aff(i)
            i += 1


class VizPrint:
    """
    Handle the printing of a graph given the root of the Graph.

    The class Graph is handled by the tasks, on instance for each task, containing data, input, output, pointers to subtask, etc...
    Uses all those information to print a graph using Digraph
    """

    def __init__(self):
        """
        __init__ Initialize a Digraph, and creates the root
        """
        self.Gr = Digraph(format="svg")
        self.Gr.graph_attr.update(ratio="expand")
        self.Gr.attr(rankdir="TB")
        self.start = Node()

    def findOut(self, g: Node) -> Node:
        """
        Resolve delegation of tasks in the graph.

        This function is used by VizPrint to fix incorrect input links caused by task delegation.

        Imagine the root task splitting `delta` into two subsets — it spawns two child tasks and a `nAGG`
        to gather their results. However, those children might delegate their work further, possibly building
        separate subtrees.

        In PymoniK, this is fine — the `nAGG` will wait for the final results and execute correctly.
        But in the visualization graph we construct locally, the `nAGG` still appears connected to the original
        children, even though they didn't produce the actual output.

        This function walks through the delegation chain to locate the real source of the result for each input
        and reconnects the `nAGG` accordingly. It ensures the printed graph reflects the true data flow.

        Because a picture is worth a thousand words, see the ASCII diagram below for a full example.

        Example :
        ```text

                          [ROOT]
                            |
                    +----------------+
                    |                |
                [TASK A]         [TASK B]
                    |                |
                    |                |
                    +---> [nAGG] <---+
                           (created by ROOT, waiting on TASK A and TASK B)

                    Imagine TASK A delegated it's result to anther task
                          [ROOT]
                            |
                   +-------------------+
                   |                   |
               [TASK A]-+           [TASK B]
                   |    |              |
               [CALC A1]|              |
                   |    |              |
               [nAGG_A] |              |
                        |              |
                        |              |
                        +->[nAGG] <----+
                            (still points to TASK A and TASK B, the graph is not correct)

                    findOut finds which node TASK A delegated to recursively (nAGG_A can delegate too)

                          [ROOT]
                            |
                   +-------------------+
                   |                   |
               [TASK A]             [TASK B]
                   |                   |
               [CALC A1]               |
                   |                   |
               [nAGG_A]                |
                   |                   |
                   |                   |
                   +-----> [nAGG] <----+
                            (perfect !)
        ```


        Args:
            g (Node): The node we want to get the output

        Returns:
            Node: The node that outputs
        """
        out = g.out[0]
        while out != out.out[0]:
            out = out.out[0]
        return out

    def TrueFalse(self, val) -> str:
        return "green" if val else "black"

    def UpColorSelector(self, g: Node) -> List[str]:
        """
        UpColorSelector For Aggregators, give the color of the edges.
        If two inputs have a common subset in their answer (which is a list of subset) color the edge in orange
        If two inputs have exactly the same answer, color the edge in red

        Note:
            This function can be use on non aggregator task and will only color the edges in black, this allows us to call it every time without determining the type of tas represented by the node (we treat each node independently of it's type of task (cf print method))

        Args:
            g (Node): The aggregator

        Returns:
            List[str]: the list of the color of edges between g and it's input
        """
        res = ["black"] * len(g.up)
        mem = {}
        mem2 = {}
        for idx, _in in enumerate(g.up):
            out = self.findOut(_in[0])

            data = out.out[1][0]
            if data is None:
                continue

            for dat in data:  # On vérifie si tous les sous ensembles de data on déjà été vus
                val = dat.__str__()
                if val not in mem2:
                    mem2[val] = [idx]
                else:
                    mem2[val].append(idx)

            data = data.__str__()
            if data not in mem:  # Qqn a-t-il déjà fait exactement la même chose ?
                mem[data] = [idx]
            else:
                mem[data].append(idx)

        for _, val in mem2.items():
            if len(val) >= 2:
                for idx in val:
                    res[idx] = "orange"

        for _, val in mem.items():
            if len(val) >= 2:
                for idx in val:
                    res[idx] = "red"
        return res

    def BuildGraph(self, g: Node):
        """
        Recursively prints the computation graph starting from the given node `g`.

        This method builds the visual representation of the graph by:
        - Adding edges from parent nodes (`g.up`) to `g`.
        - Rendering all children (`g.son`) as nodes connected through intermediate data boxes.
        - Traversing the `g.out` edge, which may lead to another task node or contain final result data.

        The function uses internal helpers (`findOut`, `UpColorSelector`, etc.) to resolve delegation,
        assign colors, and display emphasis or labels depending on the graph structure.

        Args:
            g (Graph): The root node of the graph (or subgraph) to render.
        """
        if g.up:
            color = self.UpColorSelector(g)
            i = 0
            for _in in g.up:
                out = self.findOut(_in[0])
                dataId = "d_" + out.id
                self.Gr.edge(dataId, g.id, color=color[i])
                i += 1
        if g.son:
            for _son in g.son:
                son = _son[0]
                data = _son[1]
                label = _son[2]
                self.Gr.node(son.id, son.type, color=son.emphasis)
                dataId = "i_" + son.id
                self.Gr.node(dataId, label + data.__str__(), shape="box")
                self.Gr.edge(g.id, dataId)
                self.Gr.edge(dataId, son.id)
                self.BuildGraph(son)
        if g.out[1] is None:
            if len(g.son) == 1 and g.son[0][0] == g.out[0]:
                return
            self.Gr.node(g.out[0].id, g.out[0].type, color=g.out[0].emphasis)
            self.BuildGraph(g.out[0])
        else:
            data = g.out[1]
            color = self.TrueFalse(data[1])
            data = data[0]
            self.Gr.node("d_" + g.id, data.__str__(), shape="box", fontcolor=color)
            self.Gr.edge(g.id, "d_" + g.id)

    def getGraph(self, print: bool = True):
        if print:
            return self.start
        return None

    def aff(self, idx: int):
        """
        aff Build then print the graph

        Args:
            idx (int): name the graph "graphic{idx}.svg"
        """
        self.Gr.node(self.start.id, self.start.type, color=self.start.emphasis)
        self.BuildGraph(self.start)
        self.Gr.render(f"graphic{idx}", format="svg", view=False)
