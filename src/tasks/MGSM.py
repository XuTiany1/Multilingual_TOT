import re
import os
import sympy
import pandas as pd
from src.tasks.task import Task, DATA_PATH
from datasets import load_dataset
from src.prompts.MGSM_EN import *


class MgsmTask(Task):

    def __init__(self, args):

        super().__init__()

        ################################
        # Download dataset
        data_card = "juletxara/mgsm"
        data_dir = "data/MGSM/"
        os.makedirs(data_dir, exist_ok=True)
        languages = ['en', 'es', 'fr', 'de', 'ru', 'zh', 'ja', 'th', 'sw', 'bn', 'te']

        # Download and save datasets for each language
        for curr_lang in languages:

            lang_dir = os.path.join(data_dir, curr_lang)
            train_file = os.path.join(lang_dir, "train.tsv")
            test_file = os.path.join(lang_dir, "test.tsv")

            # Skip downloading if files already exist
            if os.path.exists(train_file) and os.path.exists(test_file):
                print(f"Dataset for {curr_lang} already exists. Skipping download.")
                continue  # Skip to next language

            print(f"Downloading dataset for language: {curr_lang}")
            dataset = load_dataset(data_card, curr_lang)
            os.makedirs(lang_dir, exist_ok=True)

            # Save train and test splits as TSV files
            dataset["train"].to_pandas().to_csv(os.path.join(lang_dir, "train.tsv"), sep="\t", index=False)
            dataset["test"].to_pandas().to_csv(os.path.join(lang_dir, "test.tsv"), sep="\t", index=False)

        # Load the chosen langauge dataset
        chosen_lang = args.lang
        lang_dir = os.path.join(data_dir, chosen_lang)
        train_file = os.path.join(lang_dir, "train.tsv")
        test_file = os.path.join(lang_dir, "test.tsv")

        self.train_data = pd.read_csv(train_file, sep="\t", quoting=3)
        self.test_data = pd.read_csv(test_file, sep="\t", quoting=3)

        # Set current data into either train or test
        self.data = self.train_data

        ################################
        # Other variable initialization
        self.stops = ['\n'] * 4
        self.steps = 4
        self.value_cache = {}


    ##################
    # HELPER FUNC.
    ##################
    def set_data_split(self, split: str):
        """
        Set the current data split (train or test).
        """
        if split == "train":
            self.data = self.train_data
        elif split == "test":
            self.data = self.test_data
        else:
            raise ValueError("Invalid split. Use 'train' or 'test'.")


    def __len__(self) -> int:
        """
        Returns the number of data instances in the current split.
        """
        return len(self.data)


    def get_input(self, idx: int) -> str:
        """
        Returns the question (input) at the given index in the current split.
        """
        if idx < 0 or idx >= len(self.data):
            raise IndexError("Index out of range.")
        return self.data.iloc[idx]["question"]



    ##################
    # TO BE TESTED
    ##################
    def test_output(self, idx: int, output: str):
        """
        Tests if the output solution matches the correct numeric answer for the problem at index `idx`.

        Args:
            idx (int): Index of the problem in the dataset.
            output (str): The generated solution to evaluate.

        Returns:
            dict: {'r': 1} if the solution is correct, {'r': 0} otherwise.
        """
        # Extract the answer expression from the output
        try:
            expression = output.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
        except IndexError:
            return {'r': 0}  # Return 0 if the output format is invalid

        # Evaluate the expression and compare to the correct answer
        correct_answer = self.data.iloc[idx]["answer_number"]
        try:
            result = sympy.simplify(expression)
            return {'r': int(result == correct_answer)}
        except Exception as e:
            return {'r': 0}


    ##################
    # PROMPT
    ##################

    @staticmethod
    def standard_prompt_wrap(x: str) -> str:

        prompt = standard_prompt.format(
            question = x
        )
        return prompt

    @staticmethod
    def cot_prompt_wrap(x: str) -> str:

        prompt = cot_prompt.format(
            question = x
        )
        return prompt

    @staticmethod
    def propose_prompt_wrap(num_mathematicians: int, lang: str, x: str, y: str = '') -> str:

        prompt = propose_prompt.format(
            n = num_mathematicians,
            lang = lang,
            question = x,
            current_thought_process = y
        )

        return prompt


    @staticmethod
    def value_prompt_wrap(x:str, y: str) -> str:
        prompt = value_prompt.format(
            question = x,
            curr_candidate = y
        )

        return prompt



    @staticmethod
    def value_outputs_unwrap(value_outputs: list) -> float:
        """
        value_outputs - a list of the judgements given from model from previous evaluation on the values
        """
        return 1.1








































