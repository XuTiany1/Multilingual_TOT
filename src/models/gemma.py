import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


# Define the target directory for downloading the model
model_dir = os.path.expanduser("~src/models/downloaded_model/gemma")  # Use home directory

# Ensure the directory exists
os.makedirs(model_dir, exist_ok=True)

# Load the tokenizer and model with the specified cache directory
model_name = "google/gemma-2-27b"
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_dir)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=model_dir,  # Ensures the model is saved locally
    device_map="auto",    # Distributes across available GPUs
    torch_dtype=torch.float16  # Use float16 to optimize memory usage
    #local_files_only=True
)

def gemma_generate(prompt, max_tokens=1000, temperature=0.7, top_p=0.9):
    """
    Generates text using Gemma 2-27B.

    Args:
        prompt (str): The input prompt.
        max_tokens (int): Maximum number of tokens to generate.
        temperature (float): Sampling temperature for diversity.
        top_p (float): Top-p (nucleus) sampling for diversity.

    Returns:
        str: Generated text.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example test
if __name__ == "__main__":
    prompt = "Explain the theory of relativity in simple terms."
    response = gemma_generate(prompt)
    print(response)