import grpc

from armonik.client import ArmoniKTasks
from armonik.common import Task
from armonik.common import TaskStatus


class TasksFinder:
    """
    Helper class to find and manage ArmoniK tasks for a given session and filter.

    Provides methods to load and update tasks metadata using the ArmoniK API.
    """

    PAGE_SIZE = 1000

    def __init__(self, endpoint: str, session_id, filter) -> None:
        """
        Initialize the TasksFinder with a gRPC endpoint, session ID, and filter.
        Args:
            endpoint (str): The gRPC endpoint to connect to.
            session_id: The session ID to filter tasks.
            filter: Additional filter to apply to tasks.
        """
        self._channel = grpc.insecure_channel(endpoint)
        self._task_handler: ArmoniKTasks = ArmoniKTasks(self._channel)

        self._tasks: list[Task] = []
        self._filter = (
            (Task.session_id == session_id) & (Task.status == TaskStatus.COMPLETED) & filter
        )

        self._page: int = 0

    def __del__(self):
        """
        Destructor to close the gRPC channel when the object is deleted.
        """
        self._channel.close()

    def _load_next_page(self) -> bool:
        """
        Load the next page of tasks from the ArmoniK API and extend the internal task list.
        Returns:
            bool: True if new tasks were loaded, False otherwise.
        """
        size, tasks = self._task_handler.list_tasks(
            task_filter=self._filter,
            sort_field=Task.created_at,
            page=self._page,
            page_size=TasksFinder.PAGE_SIZE,
        )  # type: ignore
        if len(tasks) == TasksFinder.PAGE_SIZE:
            self._page += 1
        if size > len(self._tasks):
            start = len(self._tasks) % TasksFinder.PAGE_SIZE
            self._tasks.extend(tasks[start:])
            return True
        return False

    def update(self):
        """
        Update the internal task list by loading all new tasks since the last update.
        Returns:
            list[Task]: The list of newly loaded tasks.
        """
        start = len(self._tasks)
        while self._load_next_page():
            pass
        return self._tasks[start:]

    def close(self):
        """
        Close the gRPC channel explicitly.
        """
        self._channel.close()
