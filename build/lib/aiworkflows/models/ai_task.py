from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field
from aiworkflows.models.ai_task_configuration import AiTaskConfiguration
from aiworkflows.models.ai_task_input import AiTaskInput
from aiworkflows.models.ai_task_output import AiTaskOutput
from aiworkflows.models.ai_task_primitive_type import get_mapped_type


class AiTask:
    def __init__(self,
                 task_ref: str,
                 configuration: AiTaskConfiguration,
                 prompt: str,
                 output: AiTaskOutput,
                 inputs: list[AiTaskInput] = None,
                 name: str = None,
                 description: str = None,
                 task_id: str = None,
                 tenant_id: str = None,
                 ):
        self.task_ref: str = task_ref
        self.configuration: AiTaskConfiguration = configuration
        self.prompt: str = prompt
        self.output: AiTaskOutput = output
        self.inputs: list[AiTaskInput] = inputs
        self.name: str = name
        self.description: str = description
        self.task_id: str = task_id
        self.tenant_id: str = tenant_id

        self._api: "AiWorkflowsApi" = None

    def bind_api(self, api: "AiWorkflowsApi"):
        self._api = api

    @property
    def api(self) -> "AiWorkflowsApi":
        return self._api

    @staticmethod
    def from_json(json: dict):
        task_ref = parse_required_field(json, 'taskRef', str)
        configuration = parse_required_field(json, 'configuration', AiTaskConfiguration)
        prompt = parse_required_field(json, 'prompt', str)
        output = parse_required_field(json, 'output', AiTaskOutput)
        name = parse_optional_field(json, 'name', str)
        description = parse_optional_field(json, 'description', str)
        task_id = parse_optional_field(json, 'id', str)
        tenant_id = parse_optional_field(json, 'tenantId', str)

        inputs = parse_optional_field(json, 'inputs', list)
        if inputs:
            inputs = [AiTaskInput.from_json(i) for i in inputs]

        return AiTask(task_ref=task_ref,
                      configuration=configuration,
                      prompt=prompt,
                      output=output,
                      inputs=inputs,
                      name=name,
                      description=description,
                      task_id=task_id,
                      tenant_id=tenant_id)

    def to_json(self):
        return {
            'taskRef': self.task_ref,
            'configuration': self.configuration.to_json(),
            'prompt': self.prompt,
            'output': self.output.to_json(),
            'inputs': [i.to_json() for i in self.inputs] if self.inputs else None,
            'name': self.name,
            'description': self.description,
            'id': self.task_id,
            'tenantId': self.tenant_id,
        }

    def __call__(self, *args, **kwargs):
        if self.api is None:
            raise RuntimeError('Error running task: API not bound')

        inputs: dict = {}
        if self.inputs is not None:
            # bind all args in sequential order to inputs and kwargs to specific inputs
            if (len(args) + len(kwargs)) > len(self.inputs):
                raise RuntimeError(f'Error running task: too many arguments, expected {len(self.inputs)} '
                                   f'but got {len(args) + len(kwargs)}')

            for i, arg in enumerate(args):
                input_schema: AiTaskInput = self.inputs[i]

                expected_type: type = get_mapped_type(input_schema.input_type)
                if not isinstance(arg, expected_type):
                    raise RuntimeError(f'Error running task: expected argument {i} to be of type {expected_type} '
                                       f'but got {type(arg)}')

                inputs[input_schema.input_ref] = arg

            for ref, value in kwargs.items():
                input_schema: AiTaskInput = next((i for i in self.inputs if i.input_ref == ref), None)
                if input_schema is None:
                    raise RuntimeError(f'Error running task: unknown input {ref}')

                expected_type: type = get_mapped_type(input_schema.input_type)
                if not isinstance(value, expected_type):
                    raise RuntimeError(f'Error running task: expected argument {ref} to be of type {expected_type} '
                                       f'but got {type(value)}')

                inputs[ref] = value

            # make sure all required inputs are present
            for input_schema in self.inputs:
                if input_schema.is_required and input_schema.input_ref not in inputs:
                    raise RuntimeError(f'Error running task: missing required input {input_schema.input_ref}')

        return self.api.run_task(task_ref=self.task_ref, inputs=inputs)

    def run(self, *args, **kwargs):
        return self.__call__(*args, **kwargs)

    def __repr__(self):
        return f'AiTask(tenant_id={self.tenant_id}, id={self.task_id}, task_ref={self.task_ref}, ' \
               f'name={self.name}, description={self.description})'

    def __str__(self):
        return self.__repr__()


