import grpc

from armonik.client import ArmoniKTasks
from armonik.common import Task
from armonik.common import TaskStatus


class TasksFinder:
    PAGE_SIZE = 1000

    def __init__(self, endpoint: str, session_id, filter) -> None:
        self._channel = grpc.insecure_channel(endpoint)
        self._task_handler: ArmoniKTasks = ArmoniKTasks(self._channel)

        self._tasks: list[Task] = []
        self._filter = (
            (Task.session_id == session_id) & (Task.status == TaskStatus.COMPLETED) & filter
        )

        self._page: int = 0

    def __del__(self):
        self._channel.close()

    def _load_next_page(self) -> bool:
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
        start = len(self._tasks)
        while self._load_next_page():
            pass
        return self._tasks[start:]

    def close(self):
        self._channel.close()
