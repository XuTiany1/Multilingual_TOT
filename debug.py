import argparse
from src.tasks.MGSM import MgsmTask

# Simulate the arguments for MgsmTask
class Args:
    def __init__(self, chosen_lang):
        self.chosen_lang = chosen_lang

def test_mgsm_task():
    # Create arguments with the chosen language
    args = Args(chosen_lang="en")

    # Initialize the MgsmTask instance
    task = MgsmTask(args)

    # Test the __len__ method
    task.set_data_split("train")
    print(f"Number of training instances: {len(task)}")
    assert len(task) > 0, "Training dataset should not be empty."

    # Test the get_input method for the train split
    first_train_question = task.get_input(0)
    print(f"First training question: {first_train_question}")
    assert isinstance(first_train_question, str), "get_input should return a string."

    # Switch to the test split
    task.set_data_split("test")
    print(f"Number of testing instances: {len(task)}")
    assert len(task) > 0, "Testing dataset should not be empty."

    # Test the get_input method for the test split
    first_test_question = task.get_input(0)
    print(f"First testing question: {first_test_question}")
    assert isinstance(first_test_question, str), "get_input should return a string."

    print("All tests passed!")

if __name__ == "__main__":
    test_mgsm_task()