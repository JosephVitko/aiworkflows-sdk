import json
import os

from aiworkflows.api.aiworkflows_api import AiWorkflowsApi
from aiworkflows.models.ai_task import AiTask


class TaskCompiler:
    def __init__(self, api: AiWorkflowsApi):
        self.api: AiWorkflowsApi = api

    def deploy_json_tasks_from_directory(self, directory_path: str, recursive: bool = False) -> list[AiTask]:
        """
        Deploys all json tasks from a directory.
        :param directory_path:
        :param recursive:
        :return:
        """
        tasks: list[AiTask] = []

        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)

            extension = os.path.splitext(file_path)[1]
            if not extension == '.aitj':
                continue

            if os.path.isfile(file_path):
                try:
                    task: AiTask = self.deploy_task_from_json_file(file_path)
                    tasks.append(task)
                except Exception as e:
                    print(f'Failed to deploy task from file {file_path}: {e}')
            elif os.path.isdir(file_path) and recursive:
                try:
                    sub_tasks: list[AiTask] = self.deploy_json_tasks_from_directory(file_path, recursive)
                    tasks.extend(sub_tasks)
                except Exception as e:
                    print(f'Failed to deploy tasks from directory {file_path}: {e}')

        return tasks

    def deploy_task_from_json_file(self, file_path: str) -> AiTask:
        """
        Deploys a task from a json file.

        :param file_path:
        :return:
        """
        with open(file_path, 'r') as f:
            json_task = json.load(f)

        return self.deploy_json_task(json_task)

    def deploy_json_task(self, json_task: dict) -> AiTask:
        """
        Deploys a task based on its json object.
        :param json_task:
        :return:
        """
        task: AiTask = AiTask.from_json(json_task)

        # check if the task already exists
        existing_task: AiTask
        try:
            existing_task = self.api.get_task(task.task_ref)
        except Exception as e:
            existing_task = None

        if existing_task is not None:
            print(f'Task {task.task_ref} already exists. Updating...')
            task.task_id = existing_task.task_id
            task.tenant_id = existing_task.tenant_id
            return self.api.update_task(task)

        print(f'Deploying task {task.task_ref}...')
        return self.api.create_task(task)
