"""
Conciseness test
"""

import json

from .template import ConcisenessTemplate


class ConcisenessTest:
    """
    Class for testing the conciseness of your LLM response

    Returns:
    dict: Result of the evaluation including conciseness_test score, and other relevant information.

    """

    def __init__(
        self, client, prompt, response, context = None, strictness=1, model="gpt-3.5-turbo"
    ):
        """
        Initializes the test instance with the provided parameters.
        Args:
            prompt (str): The prompt for the response.
            response (str): The response to be evaluated.
            context (str): The context for the response (default is None).
            strictness (int): The number of times response is evaluated (default is 1).
            model (str): The model to be used for evaluation (default is "gpt-3.5-turbo").

        """
        self.question = prompt
        self.client = client
        self.response = response
        self.context = context
        self.model_name = model
        self.strictness = strictness
        self.strictness = (
            self.strictness if self.strictness % 2 != 0 else self.strictness + 1
        )

    def model(self, prompt):
        """
        A function to generate chat completions based on a prompt.

        Args:
            prompt (str): The prompt for generating chat completions.

        Returns:
            dict: The generated chat completions.
        """
        example_json = {
            "input": "Who is Max Verstappen?",
            "submission": "Max Verstappen is a F1 Driver",
            "criteria": "Does the submission presents ideas, information, or arguments in a logical and organized manner?",
            "output": {"verdict": "0"},
        }
        return self.client.chat.completions.create(
            model=self.model_name,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "Please provide output in valid JSON. The data schema should be like this"
                    + json.dumps(example_json),
                },
                {"role": "user", "content": prompt},
            ],
        )

    def generate_verdict(self):
        """
        Generate a verdict using the prompt, and response.
        """
        if self.context is not None:
            question = f"{self.question} answer using context: {self.context}"
        else:
          question = self.question
        return ConcisenessTemplate.generate_verdict(question, self.response)

    def evaluate(self, statement):
        """
        Generate a score for the response based on the provided criteria.
        """
        response = self.model(statement)
        return json.loads(response.choices[0].message.content)

    def generate_score(self, json_response):
        """
        Evaluate the conciseness of the response.
        """
        score = int(json_response["output"]["verdict"])
        return score

    def run(self):
        """
        Run the test and return the results.
        """
        responses = []
        for _ in range(self.strictness):
            verdict = self.generate_verdict()
            res = self.evaluate(self.response)
            responses.append(self.generate_score(res))

        passed_count = sum(score != 0 for score in responses)
        conciseness_score = 1 if passed_count > self.strictness / 2 else 0

        result = {
            "input": self.question,
            "response": self.response,
            "context": self.context,
            "is_passed": "Passed" if conciseness_score != 0 else "Failed",
            "conciseness_score": conciseness_score,
            "evaluated_with": {"model": self.model_name},
        }

        return result
