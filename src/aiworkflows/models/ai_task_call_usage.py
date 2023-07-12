from aiworkflows.compiler.utils.json_utils import parse_required_field, parse_optional_field


class AiTaskCallUsage:
    def __init__(self,
                 total_tokens: int,
                 prompt_tokens: int = None,
                 completion_tokens: int = None,
                 ):
        self.total_tokens: int = total_tokens
        self.prompt_tokens: int = prompt_tokens
        self.completion_tokens: int = completion_tokens

    @staticmethod
    def from_json(json: dict):
        total_tokens = parse_required_field(json, 'total_tokens', int)
        prompt_tokens = parse_optional_field(json, 'prompt_tokens', int)
        completion_tokens = parse_optional_field(json, 'completion_tokens', int)

        return AiTaskCallUsage(total_tokens=total_tokens,
                               prompt_tokens=prompt_tokens,
                               completion_tokens=completion_tokens)

    def to_json(self):
        return {
            'total_tokens': self.total_tokens,
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
        }

    def __repr__(self):
        return f'AiTaskCallUsage(total_tokens={self.total_tokens}, prompt_tokens={self.prompt_tokens}, completion_tokens={self.completion_tokens})'

    def __str__(self):
        return f'AiTaskCallUsage(total_tokens={self.total_tokens}, prompt_tokens={self.prompt_tokens}, completion_tokens={self.completion_tokens})'