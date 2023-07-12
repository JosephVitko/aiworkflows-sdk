import os

from aiworkflows.api import tasks
from aiworkflows.models.ai_task import AiTask
from aiworkflows.models.ai_task_execution import AiTaskExecution


class AiWorkflowsApi:
    def __init__(self, api_key: str = None, authority: str = None):
        if api_key is None:
            api_key = os.environ.get('AIWORKFLOWS_API_KEY', None)

            if api_key is None:
                raise ValueError('Error initializing AiWorkflowsApi: api_key must be provided either as a parameter '
                                 'or as an environment variable (AIWORKFLOWS_API_KEY)')

        if authority is None:
            authority = os.environ.get('AIWORKFLOWS_API_AUTHORITY', None)

            if authority is None:
                raise ValueError('Error initializing authority: api_url must be provided either as a parameter '
                                 'or as an environment variable (AIWORKFLOWS_API_AUTHORITY)')

        self.api_key: str = api_key
        self.authority: str = authority

    def create_task(self, task: AiTask) -> AiTask:
        return tasks.create_task(self, task, True)

    def update_task(self, task: AiTask) -> AiTask:
        return tasks.update_task(self, task, True)

    def get_task(self, task_ref: str) -> AiTask:
        return tasks.get_task(self, task_ref, True)

    def delete_task(self, task_ref: str) -> None:
        return tasks.delete_task(self, task_ref)

    def list_tasks(self) -> list[AiTask]:
        return tasks.list_tasks(self)

    def run_task(self, task_ref: str, inputs: dict) -> AiTaskExecution:
        return tasks.run_task(self, task_ref, inputs)









