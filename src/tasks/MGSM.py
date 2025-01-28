import re
import os
import sympy
import pandas as pd
from src.tasks.task import Task, DATA_PATH
from datasets import load_dataset


class MgsmTask(Task):

    def __init__(self, args):

        super().__init__()

        # Download dataset
        data_card = "juletxara/mgsm"
        data_dir = "data/MGSM/"
        os.makedirs(data_dir, exist_ok=True)
        languages = ['en', 'es', 'fr', 'de', 'ru', 'zh', 'ja', 'th', 'sw', 'bn', 'te']

        # Download and save datasets for each language
        for curr_lang in languages:
            print(f"Downloading dataset for language: {curr_lang}")
            dataset = load_dataset(data_card, curr_lang)
            
            # Save to disk in the corresponding directory
            lang_dir = os.path.join(data_dir, curr_lang)
            os.makedirs(lang_dir, exist_ok=True)

            # Save train and test splits as TSV files
            dataset["train"].to_pandas().to_csv(os.path.join(lang_dir, "train.tsv"), sep="\t", index=False)
            dataset["test"].to_pandas().to_csv(os.path.join(lang_dir, "test.tsv"), sep="\t", index=False)

        
        # Load the chosen langauge dataset
        chosen_lang = args.chosen_lang
        lang_dir = os.path.join(data_dir, chosen_lang)
        train_file = os.path.join(lang_dir, "train.tsv")
        test_file = os.path.join(lang_dir, "test.tsv")

        train_df = pd.read_csv(train_file, sep="\t", quoting=3)
        test_df = pd.read_csv(test_file, sep="\t", quoting=3)

        print(train_df.head())
        print("---------------------------------------")
        print("---------------------------------------")
        print("---------------------------------------")
        print(test_df.head())