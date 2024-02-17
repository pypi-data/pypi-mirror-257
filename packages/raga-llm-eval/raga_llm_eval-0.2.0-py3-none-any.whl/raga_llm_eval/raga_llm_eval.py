"""
Main Function for RagaLLMEval
"""

import json
import os
import pkgutil
import warnings

import toml
from openai import OpenAI
from prettytable import ALL, PrettyTable

from .llm_tests.test_executor import TestExecutor
from .utils.utils import NumpyEncoder


class RagaLLMEval:
    """
    Class for managing the API keys and executing tests.
    """

    def __init__(self, api_keys=None):
        """
        Constructor for the API key manager.

        Args:
            api_keys (dict, optional): A dictionary containing API keys for
                            OpenAI and Hugging Face Hub. Defaults to None.

        Attributes:
            __open_ai_api_key (str): The OpenAI API key.
            __hugging_face_hub_api_token (str): The Hugging Face Hub API token.
            supported_tests (dict): A dictionary containing descriptions and
                                    expected arguments for supported tests.
            _test_methods (dict): A dictionary mapping test names to their
                                  corresponding methods.
            _tests_to_execute (list): A list of test names to be executed.
            _results (list): A list to store the results of the executed tests.
        """
        self.__set_api_keys(api_keys=api_keys)

        self._results = []
        self._tests_to_execute = []
        self._output_format = "summary"
        self._openai_client = self.__set_openai_client()
        self._supported_tests = self._load_supported_tests()

        self._test_executor = TestExecutor(openai_client=self._openai_client)

        self._test_methods = {
            "relevancy_test": self._test_executor.run_relevancy_test,
            "bias_test": self._test_executor.run_bias_test,
            "contextual_precision_test": self._test_executor.run_contextual_precision_test,
            "contextual_recall_test": self._test_executor.run_contextual_recall_test,
            "contextual_relevancy_test": self._test_executor.run_contextual_relevancy_test,
            "faithfulness_test": self._test_executor.run_faithfulness_test,
            "maliciousness_test": self._test_executor.run_maliciousness_test,
            "summarisation_test": self._test_executor.run_summarisation_test,
            "coherence_test": self._test_executor.run_coherence_test,
            "conciseness_test": self._test_executor.run_conciseness_test,
            "refusal_test": self._test_executor.run_refusal_test,
            "correctness_test": self._test_executor.run_correctness_test,
            "consistency_test": self._test_executor.run_consistency_test,
            "length_test": self._test_executor.run_length_test,
            "cover_test": self._test_executor.run_cover_test,
            "pos_test": self._test_executor.run_pos_test,
            "response_toxicity_test": self._test_executor.run_response_toxicity_test,
            "toxicity_test": self._test_executor.run_toxicity_test,
            "winner_test": self._test_executor.run_winner_test,
            "overall_test": self._test_executor.run_overall_test,
            "prompt_injection_test": self._test_executor.run_prompt_injection_test,
            "sentiment_analysis_test": self._test_executor.run_sentiment_analysis_test,
            # "violence_check_test": self.test_executor.run_harmless_test,
            "hallucination_test": self._test_executor.run_hallucination_test,
            "generic_evaluation_test": self._test_executor.run_generic_evaluation_test,
            "complexity_test": self._test_executor.run_complexity_test,
            "cosine_similarity_test": self._test_executor.run_cosine_similarity_test,
            "grade_score_test": self._test_executor.run_grade_score_test,
            "readability_test": self._test_executor.run_readability_test,
        }

        self.__welcome_message()

    def __welcome_message(self):
        print("🌟 Welcome to raga_llm_eval! 🌟")
        print(
            "The most comprehensive LLM (Large Language Models) testing library at your service."
        )

    def _load_supported_tests(self):
        """
        Load supported tests from the test details TOML file and return the supported tests.
        """
        data = pkgutil.get_data("raga_llm_eval", "llm_tests/test_details.toml")
        if data is not None:  # Check if data was successfully loaded
            data_str = data.decode("utf-8")  # Decode bytes to string
            self._supported_tests = toml.loads(data_str)
        else:
            raise FileNotFoundError("Could not load the test_details.toml file.")

        return self._supported_tests

    def __set_api_keys(self, api_keys):
        """
        Set the API keys for OpenAI and Hugging Face Hub.

        Parameters:
            api_keys (dict): A dictionary containing the API keys for OpenAI and Hugging Face Hub.

        Returns:
            None
        """
        open_ai_api_key = (
            api_keys.get("OPENAI_API_KEY")
            if api_keys and "OPENAI_API_KEY" in api_keys
            else os.getenv("OPENAI_API_KEY", None)
        )
        hugging_face_hub_api_token = (
            api_keys.get("HUGGINGFACEHUB_API_TOKEN")
            if api_keys and "HUGGINGFACEHUB_API_TOKEN" in api_keys
            else os.getenv("HUGGINGFACEHUB_API_TOKEN", None)
        )

        if open_ai_api_key:
            os.environ["OPENAI_API_KEY"] = open_ai_api_key

        if hugging_face_hub_api_token:
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_hub_api_token

        os.environ["TOKENIZERS_PARALLELISM"] = "true"

    # set and get openai client
    def __set_openai_client(self):
        if os.getenv("OPENAI_API_KEY"):
            return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        raise ValueError("OPENAI_API_KEY needs to be set.")

    def list_available_tests(self):
        """
        List available tests and their details in a formatted table.
        """
        print(
            "📋 Below is the list of tests currently supported by our system. Stay tuned for more updates and additions!"
        )

        table = PrettyTable()
        table.field_names = [
            "SNo.",
            "Test Name",
            "Description",
            # "Expected Arguments",
            # "Expected Output",
            # "Interpretation",
        ]

        try:
            for field_name in table.field_names:
                table.max_width[field_name] = {
                    "SNo.": 5,
                    "Test Name": 25,
                    "Description": 50,
                    # "Expected Arguments": 20,
                    # "Expected Output": 20,
                    # "Interpretation": 20,
                }.get(field_name, 20)
        except AttributeError:
            # pylint: disable=protected-access
            table._max_width = {
                "SNo.": 5,
                "Test Name": 25,
                "Description": 50,
                # "Expected Arguments": 20,
                # "Expected Output": 20,
                # "Interpretation": 20,
            }
        table.hrules = ALL

        for idx, (test_name, details) in enumerate(
            self._supported_tests.items(), start=1
        ):  # Start indexing from 1 for better readability
            table.add_row(
                [
                    idx,
                    test_name,
                    details["description"],
                    # str(details["expected_arguments"]),
                    # str(details["expected_output"]),
                    # details["interpretation"],
                ]
            )

        print(table)

    def add_test(
        self,
        test_names,
        data,
        arguments=None,
    ):
        """
        Add a test to the execution queue with the given parameters and return the modified instance of the object.

        Parameters:
            test_names (str or list): The name of the test or a list of test names to be added.
            test_data (dict): A dictionary containing the prompt, response, expected_response, context, and concept_set for the test.
            test_arguments (dict, optional): Additional arguments for the test (default is None).

        Returns:
            self: The modified instance of the object with the test added to the execution queue.
        """
        # Flush the previous test results and test names
        self._results = []
        self._tests_to_execute = []

        # Ensure inputs are in list form for uniform processing
        for key in data.keys():
            # ensure concept set is a list
            if key == "concept_set":
                if not isinstance(data[key], list):
                    raise ValueError("concept_set must be a list")

            if not isinstance(data[key], list):
                data[key] = [data[key]]

            if data[key] == [None]:
                data[key] = []

        # check if any of these is not present in the dict
        for val in [
            "prompt",
            "response",
            "expected_response",
            "context",
            "concept_set",
        ]:
            if val not in data.keys():
                data[val] = []

        # Validate test names
        unsupported_tests = set(test_names) - set(self._supported_tests.keys())
        if unsupported_tests:
            raise ValueError(
                f"Unsupported test(s): {unsupported_tests}. Supported tests: {list(self._supported_tests.keys())}."
            )

        prompt = data["prompt"]
        response = data["response"]
        expected_response = data["expected_response"]
        context = data["context"]
        concept_set = data["concept_set"]

        # handle none values
        max_length = max(
            len(x)
            for x in [prompt, response, expected_response, context]
            if x is not None
        )

        prompt = [None] * max_length if len(prompt) == 0 else prompt
        response = [None] * max_length if len(response) == 0 else response
        expected_response = (
            [None] * max_length if len(expected_response) == 0 else expected_response
        )
        context = [None] * max_length if context is None else context
        # if context is empty, fill it with None
        if len(context) == 0:
            context = [None] * max_length
        # if context has only a single element, make it a list
        if isinstance(context, list) and len(context) == 1:
            context = context * max_length

        # Add each test to the execution queue
        for cur_prompt, cur_response, cur_expected_response, cur_context in zip(
            prompt, response, expected_response, context
        ):
            for test_name in test_names:
                self._tests_to_execute.append(
                    {
                        "test_name": test_name,
                        "prompt": cur_prompt,
                        "response": cur_response,
                        "expected_response": cur_expected_response,
                        "context": cur_context,
                        "concept_set": concept_set,
                        "test_arguments": arguments or {},
                    }
                )

        return self

    def set_output_format(self, output_format):
        """
        Set the output format for the object.

        Parameters:
            output_format (str): The desired output format, can be 'detailed' or 'summary'.

        Returns:
            self: The updated object with the new output format.
        """
        # check if output format is one of detailed or summary, share warning with the user and use output_format="summary"
        if output_format not in ["detailed", "summary"]:
            warnings.warn(
                f"Output format {output_format} is not supported. Supported output formats are 'detailed' and 'summary'"
            )

        self._output_format = output_format

        return self

    def run(self):
        """
        Run the tests in the test suite.
        """
        if not self._tests_to_execute:
            raise ValueError("🚫 No tests to execute.")

        # Start message
        total_tests = sum(
            (
                len(test_details["test_name"])
                if isinstance(test_details["test_name"], list)
                else 1
            )
            for test_details in self._tests_to_execute
        )
        print(f"🚀 Starting execution of {total_tests} tests...")

        test_counter = 0  # Initialize a counter for the tests
        for test_details in self._tests_to_execute:
            test_names = test_details["test_name"]
            if isinstance(test_names, str):
                test_names = [test_names]

            for each_test in test_names:
                test_counter += 1  # Increment the test counter
                print(
                    f"\n🔍 Test {test_counter} of {total_tests}: {each_test} starts..."
                )  # Show the count and name of the test

                if each_test in self._test_methods:
                    method = self._test_methods[each_test]
                    result = method(test_details)
                    result["test_name"] = each_test
                    self._results.append(result)
                    print(f"✅ Test completed: {each_test}.")
                else:
                    warnings.warn(
                        f"⚠️ Warning: Test method for {each_test} not implemented."
                    )

        # End message
        print(f"✨ All tests completed. Total tests executed: {test_counter}.")

        return self

    def print_results(self):
        """
        A method to print the results in a pretty table format, creating a separate table for each test type,
        and mapping internal key names to user-friendly column names for display.
        """

        if not self._results:
            raise ValueError("🚫 No results to print.")

        # Mapping of internal key names to display names
        key_name_mapping = {
            "test_name": "Test Name",
            "prompt": "Prompt",
            "response": "Response",
            "evaluated_with": "Parameters",
            "score": "Score",
            "is_passed": "Result",
            "threshold": "Threshold",
            "context": "Context",
            "concept_set": "Concept Set",
            "test_arguments": "Test Arguments",
            "expected_response": "Expected Response",
        }

        # Group data by test names
        test_groups = {}
        for test_data in self._results:
            test_name = test_data.get("test_name", "Unknown Test Name")
            if test_name not in test_groups:
                test_groups[test_name] = []
            test_groups[test_name].append(test_data)

        # Iterate over each test group and create a table
        for test_name, test_datas in test_groups.items():
            print(f"\nTest Name: {test_name}\n")

            # Determine keys actually used in test_datas
            used_keys = set()
            for test_data in test_datas:
                used_keys.update(test_data.keys())

            # Preserve order of keys as in key_name_mapping but filter out unused keys
            field_names = [
                display_name
                for key, display_name in key_name_mapping.items()
                if key in used_keys
            ]

            table = PrettyTable()
            table.field_names = field_names

            # pylint: disable=protected-access
            table._max_width = {name: 25 for name in field_names}
            table.hrules = ALL

            for test_data in test_datas:
                row = []
                for key in key_name_mapping:  # Ensure order and filter used keys
                    if key in used_keys:
                        value = test_data.get(key, "")

                        if isinstance(value, bool):
                            row.append("✅" if value else "❌")
                        elif isinstance(value, (int, float)):
                            row.append(f"{value:.2f}")
                        elif (
                            key == "evaluated_with"
                        ):  # Special formatting for evaluated_with
                            value = ", ".join([f"{k}: {v}" for k, v in value.items()])
                            row.append(value)
                        else:
                            row.append(value)
                table.add_row(row)

            print(table)

        return self

    def get_results(self):
        """
        Get the results of the tests.

        Returns:
            The results of the tests.
        """

        if not self._results:
            raise ValueError("🚫 No results to return.")

        return self._results

    def save_results(self, file_path):
        """
        Save the results to a specified file in JSON format.

        Args:
            file_path (str): The path to the file where the results will be saved.

        Returns:
            None
        """
        if not self._results:
            raise ValueError("🚫 No results to save.")

        # Convert the results dictionary to a JSON string using the custom encoder
        results_json = json.dumps(self._results, indent=4, cls=NumpyEncoder)

        # Write the JSON string to the specified file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(results_json)

        print(f"Results saved to {file_path}")
