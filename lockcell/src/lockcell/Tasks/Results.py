from dataclasses import dataclass
from pymonik import Pymonik, ResultHandle


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

    def __post_init__(self):
        if self.failing_subset_list is None:
            self.failing_subset_list = []


@dataclass
class RDDMinResult:
    """
    A class representing the return value of the tasks

    Args:
       iteration_result : a pointer to the actual result in Armonik
       next : a pointer to the next iteration of RDDMin
    """

    iteration_result: ResultHandle[TaskResult]
    next: ResultHandle["FakeRDDMinResult"] | None


@dataclass
class FakeResult:
    """
    A dataclass containing all the information to retrieve a result from a given PymoniK object
    """

    result_id: str
    session_id: str


@dataclass
class FakeRDDMinResult:
    """
    A class representing a RDDMinResult that can be passed through cloudpickle

    Cloudpickle cannot pass ResultHandles between tasks and client, so I save both of them as FakeResult that can be passed

    Args:
       iteration_result (FakeResult): a pointer to the actual result in Armonik
       next (FakeResult): a pointer to the next iteration of RDDMin
    """

    iteration_result: FakeResult
    next: FakeResult | None


def fake_result(real: RDDMinResult) -> FakeRDDMinResult:
    """
    Transforms a RDDMinResult in a FakeRDDMinResult

    Args:
        real (RDDMinResult): The result to transform

    Returns:
        FakeRDDMinResult: The FakeRDDMinResult of 'real'
    """
    iteration_result = FakeResult(real.iteration_result.result_id, real.iteration_result.session_id)
    if real.next:
        next = FakeResult(real.next.result_id, real.next.session_id)
    else:
        next = None
    return FakeRDDMinResult(iteration_result, next)  # type: ignore


def unfake_result(fake: FakeRDDMinResult, pymonik_instance: Pymonik) -> RDDMinResult:
    """
    Transform a FakeRDDMinResult into a RDDMinResult
    Note that you need to give the pymonik_instance were the RDDMinResult

    Args:
        fake (FakeRDDMinResult): The result to transform
        pymonik_instance (Pymonik): The pymonik_instance in which the original result was created

    Returns:
        RDDMinResult: The real RDDMinResult designated by fake
    """
    iteration_result = ResultHandle(
        result_id=fake.iteration_result.result_id,
        session_id=fake.iteration_result.session_id,
        pymonik_instance=pymonik_instance,
    )
    if fake.next:
        next = ResultHandle(
            result_id=fake.next.result_id,
            session_id=fake.next.session_id,
            pymonik_instance=pymonik_instance,
        )
    else:
        next = None
    return RDDMinResult(iteration_result, next)
