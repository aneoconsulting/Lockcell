from dataclasses import dataclass
from pymonik import ResultHandle

@dataclass
class TaskResult:
    """
     A class representing the return value of the tasks

     Args:
        failing_subset_list : a list that contains all the failing subsets of the delta list that were provided to the task
        test_of_delta : indicates if the test on the whole delta list failed or not
    """
    failing_subset_list: list[list]
    test_of_delta: bool

@dataclass
class RDDMinResult:
    """
     A class representing the return value of the tasks

     Args:
        iteration_result : a pointer to the actual result in Armonik
        next : a pointer to the next iteration of RDDMin
    """
    iteration_result: ResultHandle[TaskResult]
    next: ResultHandle["RDDMinResult"] | None
