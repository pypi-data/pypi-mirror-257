from typing import Optional

from tensorfuse_python.testing.constants import value, name, evaluator_type, eval_model
from tensorfuse_python.testing.evaluators.evaluator import PythonEvaluator, Evaluator
from tensorfuse_python.testing.evaluators.model_graded_evaluations.model_graded_evaluator import LLMRubricEvaluator


def get_evaluator(eval_type, config, provider_api_key:Optional[str]=None) -> Evaluator:
    if eval_type == 'python':
        if value in config:
            function = config[value]
        else:
            raise ValueError('function is required for python evaluator')
        return PythonEvaluator(name=config[name], type=config[evaluator_type], function=function)
    if eval_type == 'llm-rubric':
        if not provider_api_key:
            raise ValueError('api_key is required for llm-rubric evaluator')
        if value in config:
            criteria = config[value]
        else:
            raise ValueError('criteria is required for llm-rubric evaluator')
        evaluator = config[eval_model] if eval_model in config else 'gpt-4'
        return LLMRubricEvaluator(name=config[name], type=config[evaluator_type], model=evaluator,
                                  criteria=criteria, api_key=provider_api_key)
    else:
        raise NotImplementedError()