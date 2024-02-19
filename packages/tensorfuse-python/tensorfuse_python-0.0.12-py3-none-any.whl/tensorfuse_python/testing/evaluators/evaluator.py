from typing import Tuple, Optional

class Evaluator:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def evaluate(self, data) -> Tuple[bool, str]:
        raise NotImplementedError


class PythonEvaluator(Evaluator):
    def __init__(self, name, type, function):
        self.function = function
        super().__init__(name, type)

    def evaluate(self, data) -> Tuple[bool, str]:
        result = self.function(data)
        return result, f'''PythonEvaluator: {self.name} evaluated {result}'''
