"""
Created on : 2025-07-07
Author   : Erwan Tchaleu
Email    : erwan.tchale@gmail.com

"""


from abc import ABC, abstractmethod



class Config(ABC):
    def __init__(self, nbRun = None):
        self.nbRun = 1
        if nbRun != None:
            self.nbRun = nbRun
        self.mode = "default"
        pass
    
    def setMode(self, mode):
        self.mode = mode

    
    @abstractmethod
    def Test(self, subspace) -> bool:
        pass

    def setNbRun(self, nbRun):
        self.nbRun = nbRun
        return self
    
    @abstractmethod
    def copy(self) -> "Config":
        pass

    
    
        

verb = False


def verbose(tab : list, end =None): # type: ignore
    if end == None:
        end = ""
    if verb:
        for p in tab:
            print(p, end =end)
        print() 
      


# List manipulers

def split(tab : list, n: int):
    """Stub to overload in subclasses"""
    subsets = []
    start = 0
    for i in range(n):
        subset = tab[start:start + (len(tab) - start) // (n - i)]
        subsets.append(subset)
        start = start + len(subset)
    return subsets

def listminus(c1 :list, c2 :list):
    """Return a list of all elements of C1 that are not in C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1

    c = []
    for delta in c1:
        if not delta in s2:
            c.append(delta)

    return c