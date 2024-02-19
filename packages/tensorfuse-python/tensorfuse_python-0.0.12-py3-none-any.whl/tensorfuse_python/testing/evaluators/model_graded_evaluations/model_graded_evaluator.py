from typing import Tuple

from openai import OpenAI

from tensorfuse_python.testing.evaluators.evaluator import Evaluator


def perform_openai_completion(model, system_prompt, user_prompt, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": system_prompt},
                                                                     {"role": "user", "content": user_prompt}],
                                              temperature=0, )
    return response.choices[0].message.content


class ModelGradedEvaluator(Evaluator):
    def __init__(self, evaluator_model: str, name: str, type: str, api_key: str):
        self.model = evaluator_model
        self.api_key = api_key
        super().__init__(name=name, type=type)

    def evaluate(self, data):
        raise NotImplementedError('ModelGradedEvaluator.evaluate() is not implemented')


class LLMRubricEvaluator(ModelGradedEvaluator):
    def __init__(self, name: str, type: str, model: str, criteria: str, api_key: str):
        self.criteria = criteria
        super().__init__(evaluator_model=model, name=name, type=type, api_key=api_key)

    def parse_response_for_reason_and_result(self, response):
        # Now the last two lines of the response should either be "Pass: True" or "Pass: False"
        # If the last line is "Pass: True", then the second last line should be "Pass: True"
        # If the last line is "Pass: False", then the second last line should be "Pass: False"
        # everything else is the reason
        # just get last line for result and everything else for reason
        response_lines = response.split('\n')
        result = response_lines[-1].strip().split(' ')[-1]
        # cast result to boolean
        if result == 'True':
            result = True
        else:
            result = False
        reason = '\n'.join(response_lines[:-2])
        return reason, result

    def evaluate(self, data) -> Tuple[bool, str]:
        LLM_RUBRIC_SYSTEM_PROMPT = '''
        You are grading output according to a user-specified rubric. If the statement in the rubric is true,
        then the output passes the test.
        '''
        LLM_RUBRIC_USER_PROMPT = '''
        Does the output satisfy the rubric? First, write out in a step by step manner your reasoning about the criterion
        to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset.
        Then print only the single character "Pass: True" or "Pass: Fail" (without quotes or punctuation) on its
        own line corresponding to the correct answer. At the end, repeat just the letter again by itself on a new line.
        
        ***Examples:***

        Output: Hello world
        Rubric: Content contains a greeting
        Reason: The content contains the word 'hello'
        Pass: True
        Pass: True
        
        Output: Avast ye swabs, repel the invaders!
        Rubric: Does not speak like a pirate
        Reason: 'avast ye' is a common pirate term
        Pass: False
        Pass: False
        
        ***User Data:***
        Output: {data}
        Rubric: {criteria}
        Reason:'''

        system_prompt = LLM_RUBRIC_SYSTEM_PROMPT
        user_prompt = LLM_RUBRIC_USER_PROMPT.format(data=data, criteria=self.criteria)
        response = perform_openai_completion(self.model, system_prompt, user_prompt, self.api_key)
        reason, result = self.parse_response_for_reason_and_result(response)
        return result, reason
