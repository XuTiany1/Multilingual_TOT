import argparse
from src.tasks.MGSM import MgsmTask

# Define a simple argument parser to simulate input arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Test MgsmTask")
    parser.add_argument('--chosen_lang', type=str, default='en', help="Language for the dataset")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse the arguments
    args = parse_args()

    # Initialize and test the MgsmTask class
    print("Testing MgsmTask...")
    task = MgsmTask(args)
    print("MgsmTask initialization complete.")