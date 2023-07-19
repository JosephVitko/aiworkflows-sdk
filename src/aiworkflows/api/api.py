import os

from dotenv import find_dotenv, load_dotenv

from aiworkflows.api import tasks
from aiworkflows.models.ai_task import AiTask
from aiworkflows.models.ai_task_execution import AiTaskExecution


class AiWorkflowsApi:
    def __init__(self, api_key: str = None, authority: str = None):
        """
        Create a new instance of the AiWorkflowsApi
        :param api_key: The API key to use for authentication
        :param authority: The authority to use for calling the API
        """
        # load .env variables
        load_dotenv(find_dotenv())

        if api_key is None:
            api_key = os.getenv('AIWORKFLOWS_API_KEY', None)

            if api_key is None:
                raise ValueError('Error initializing AiWorkflowsApi: api_key must be provided either as a parameter '
                                 'or as an environment variable (AIWORKFLOWS_API_KEY)')

        if authority is None:
            authority = os.getenv('AIWORKFLOWS_API_AUTHORITY', None)

            if authority is None:
                raise ValueError('Error initializing authority: api_url must be provided either as a parameter '
                                 'or as an environment variable (AIWORKFLOWS_API_AUTHORITY)')

        self.api_key: str = api_key
        self.authority: str = authority
        self.task_cache: dict[str, AiTask] = {}

    def create_task(self, task: AiTask, use_cache: bool = True) -> AiTask:
        """
        Create a new task in the AiWorkflows service
        :param task: The task to create
        :param use_cache: Whether to cache the task locally
        :return: The created task
        """
        task: AiTask = tasks.create_task(self, task, True)

        if use_cache:
            self.task_cache[task.task_ref] = task

        return task

    def update_task(self, task: AiTask, use_cache: bool = True) -> AiTask:
        """
        Update an existing task in the AiWorkflows service
        :param task: The task to update
        :param use_cache: Whether to cache the task locally
        :return: The updated task
        """
        task: AiTask = tasks.update_task(self, task, True)

        if use_cache:
            self.task_cache[task.task_ref] = task

        return task

    def get_task(self, task_ref: str, use_cache: bool = True) -> AiTask:
        """
        Get a task from the AiWorkflows service
        :param task_ref: The task reference to get
        :param use_cache: Whether to allow the task to be retrieved from the local cache
        """
        if use_cache and task_ref in self.task_cache:
            return self.task_cache[task_ref]

        task: AiTask = tasks.get_task(self, task_ref, True)

        if use_cache:
            self.task_cache[task_ref] = task

        return tasks.get_task(self, task_ref, True)

    def delete_task(self, task_ref: str, use_cache: bool = True) -> None:
        """
        Delete a task from the AiWorkflows service
        :param task_ref: The task reference to delete
        :param use_cache: Whether to delete the task from the local cache
        """
        tasks.delete_task(self, task_ref)

        if use_cache and task_ref in self.task_cache:
            del self.task_cache[task_ref]

    def list_tasks(self, use_cache: bool = True) -> list[AiTask]:
        """
        List all tasks in the AiWorkflows service
        :param use_cache: Whether to allow the tasks to be retrieved from the local cache
        :return: A list of all tasks
        """
        t: list[AiTask] = tasks.list_tasks(self)

        if use_cache:
            for task in t:
                self.task_cache[task.task_ref] = task

        return t

    def run_task(self, task_ref: str, inputs: dict) -> AiTaskExecution:
        """
        Run a task in the AiWorkflows service
        """
        return tasks.run_task(self, task_ref, inputs)
