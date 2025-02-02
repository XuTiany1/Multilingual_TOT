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
        self.data = self.test_data

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
    def ground_truth_answer(self, idx: int):
        """
        output answer
        """
        print(self.data.iloc[idx])
        print(self.data.iloc[idx]["answer_number"])
        return self.data.iloc[idx]["answer_number"]
    
    # Normalize the outputs by removing non-numeric characters and extra spaces
    def model_answer(self, answer):
        answer = str(answer).strip().lower()  # Ensure it's a string and normalize case
        answer = re.sub(r"[^\d.]", "", answer)  # Remove non-numeric characters except '.'


        try:
            return int(float(answer))  # Converts to float first, then int to remove decimals
        except ValueError:
            return None  # Return None if no valid number is found


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
    def value_outputs_unwrap(value_outputs: str) -> float:
        """
        Extracts the model's evaluation judgment (sure, likely, impossible) 
        in multiple languages and converts it into a numerical value.

        Args:
            value_outputs (str): Model's response containing the evaluation.

        Returns:
            float: Numeric value corresponding to the evaluation.
        """
        print(f"[DEBUG] Raw Value Output: {repr(value_outputs)}")

        # Normalize output (strip leading/trailing whitespace and convert to lowercase)
        value_outputs = value_outputs.strip().lower()

        # Multi-language mapping of judgments to numeric values
        multilang_eval_mapping = {
            # English
            "sure": 1.0, "likely": 0.5, "impossible": 0.0,
            # French
            "sûr": 1.0, "probable": 0.5, "impossible": 0.0,
            # Bengali
            "নিশ্চিত": 1.0, "সম্ভাব্য": 0.5, "অসম্ভব": 0.0,
            # German
            "sicher": 1.0, "wahrscheinlich": 0.5, "unmöglich": 0.0,
            # Spanish
            "seguro": 1.0, "probable": 0.5, "imposible": 0.0,
            # Japanese
            "確実": 1.0, "可能性あり": 0.5, "不可能": 0.0,
            # Russian
            "верно": 1.0, "вероятно": 0.5, "невозможно": 0.0,
            # Swahili
            "hakika": 1.0, "huenda": 0.5, "haiwezekani": 0.0,
            # Telugu
            "ఖచ్చితంగా": 1.0, "బహుశా": 0.5, "అసాధ్యం": 0.0,
            # Thai
            "แน่นอน": 1.0, "น่าจะเป็นไปได้": 0.5, "เป็นไปไม่ได้": 0.0,
            # Chinese (Simplified)
            "确定": 1.0, "可能": 0.5, "不可能": 0.0
        }

        # Regex pattern to match any of the known judgment words
        pattern = r"\b(" + "|".join(re.escape(k) for k in multilang_eval_mapping.keys()) + r")\b"

        # Search for the first matching judgment
        match = re.search(pattern, value_outputs)
        if match:
            return multilang_eval_mapping[match.group(1)]  # Convert to numerical value

        return 0.5  # Default if no valid judgment is found
    
    @staticmethod
    def force_output_prompt_wrap(x: str, y: str):
        prompt = force_output_prompt.format(
            question = x,
            context = y
        )

        return prompt



    @staticmethod
    def final_judgement_wrap(x: str, ys: str):
        prompt = final_judge_prompt.format(
            question=x,
            candidate_answers=ys
        )

        return prompt






































