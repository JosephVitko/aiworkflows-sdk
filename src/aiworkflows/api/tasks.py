from aiworkflows.api.utils.request_handler import send_request
from aiworkflows.models.ai_task import AiTask
from aiworkflows.models.ai_task_execution import AiTaskExecution

_task_route = '/task'


def create_task(api: "AiWorkflowsApi",
                task: AiTask,
                auto_bind_api: bool = True
                ) -> AiTask:
    """
    Creates a new task on the server.
    :param api:
    :param task:
    :param auto_bind_api: Whether to automatically bind the api to the task.
    :return:
    """
    if task.task_id:
        raise ValueError('Error creating task: task already has an id, please use update_task instead.')

    url = api.authority + _task_route + '/create'
    body = task.to_json()
    body['ref'] = body.pop('taskRef')

    response = send_request(url, api.api_key, body, method='POST', req_description='creating task')

    try:
        task: AiTask = AiTask.from_json(response)
        if auto_bind_api:
            task.bind_api(api)
        return task
    except Exception as e:
        raise RuntimeError(f'Error creating task: parsing json failed for response: {e}')


def update_task(api: "AiWorkflowsApi",
                task: AiTask,
                auto_bind_api: bool = True
                ) -> AiTask:
    """
    Updates an existing task on the server.
    :param api:
    :param task:
    :param auto_bind_api: Whether to automatically bind the api to the task.
    :return:
    """
    if not task.task_id:
        raise ValueError('Error updating task: task does not have an id, please use create_task instead.')

    if not task.tenant_id:
        raise ValueError('Error updating task: task does not have a tenant id, please use create_task instead.')

    url = api.authority + _task_route + '/update'

    body = task.to_json()
    body['ref'] = body.pop('taskRef')
    response = send_request(url, api.api_key, body, method='POST', req_description='updating task')

    try:
        task: AiTask = AiTask.from_json(response)
        if auto_bind_api:
            task.bind_api(api)
        return task
    except Exception as e:
        raise RuntimeError(f'Error updating task: parsing json failed for response: {e}')


def get_task(api: "AiWorkflowsApi",
             task_ref: str,
             auto_bind_api: bool = True
             ) -> AiTask:
    """
    Gets an existing task from the server.
    :param api:
    :param task_ref:
    :param auto_bind_api: Whether to automatically bind the api to the task.
    :return:
    """
    url = api.authority + _task_route

    body = {
        'Ref': task_ref,
    }
    response = send_request(url, api.api_key, body, method='POST', req_description='getting task')

    try:
        task: AiTask = AiTask.from_json(response)
        if auto_bind_api:
            task.bind_api(api)
        return task
    except Exception as e:
        raise RuntimeError(f'Error getting task: parsing json failed for response: {e}')


def delete_task(api: "AiWorkflowsApi",
                task_ref: str
                ) -> None:
    """
    Deletes an existing task from the server.
    :param api:
    :param task_ref:
    :return:
    """
    url = api.authority + _task_route

    body = {
        'Ref': task_ref,
    }
    send_request(url, api.api_key, body, method='POST', req_description='deleting task')


def list_tasks(api: "AiWorkflowsApi"
               ) -> list[AiTask]:
    """
    Lists tasks from the server for the current tenant.
    :param api
    :return:
    """
    url = api.authority + _task_route + '/list'

    body = {}
    response = send_request(url, api.api_key, body, method='POST', req_description='listing tasks')

    try:
        tasks: list[AiTask] = [AiTask.from_json(task_json) for task_json in response]
        for task in tasks:
            task.bind_api(api)
        return tasks
    except Exception as e:
        raise RuntimeError(f'Error listing tasks: parsing json failed for response: {e}')


def run_task(api: "AiWorkflowsApi",
             ref: str,
             inputs: dict = None
             ) -> AiTaskExecution:
    """
    Runs an existing task on the server.
    :param api:
    :param ref:
    :param inputs:
    :return:
    """
    url = api.authority + _task_route + '/run'

    if inputs is None:
        inputs = {}

    body = {
        'Ref': ref,
        'Inputs': inputs,
    }

    response = send_request(url, api.api_key, body, method='POST', req_description='running task')

    try:
        task_execution: AiTaskExecution = AiTaskExecution.from_json(response)
        return task_execution
    except Exception as e:
        raise RuntimeError(f'Error running task: parsing json failed for response: {e}')

