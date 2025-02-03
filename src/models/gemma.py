import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


os.environ["CUDA_VISIBLE_DEVICES"] = "2"

print(f"CUDA_VISIBLE_DEVICES set to: {os.environ.get('CUDA_VISIBLE_DEVICES')}")


assert torch.cuda.device_count() == 1, f"Expected only 1 visible GPU, found {torch.cuda.device_count()}."


# Check if GPU is available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32  # Use FP16 on GPU


print(f"Using device: {device}")
print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
print(f"Allocated GPU Memory: {torch.cuda.memory_allocated(device)}")
print(f"Reserved GPU Memory: {torch.cuda.memory_reserved(device)}")

# Debug: Check GPU mapping
print(f"Available GPUs in this process: {torch.cuda.device_count()}")
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

# Define the model directory
model_dir = os.path.expanduser("~/Tianyi/Multilingual_TOT/models/gemma-2-9b-it")

# Ensure the directory exists
os.makedirs(model_dir, exist_ok=True)

# Model name
model_name = "google/gemma-2-9b-it"

# Load tokenizer and model
if not os.path.exists(os.path.join(model_dir, "config.json")):
    print("Downloading and saving the model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=model_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, cache_dir=model_dir, torch_dtype=torch_dtype
    )

    # Save model locally
    tokenizer.save_pretrained(model_dir)
    model.save_pretrained(model_dir)
    print(f"Model saved to: {model_dir}")
else:
    print("Loading model from local directory...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, torch_dtype=torch_dtype, local_files_only=True
    )

# Move model to the correct device and set to evaluation mode
print(f"Using device: {device}")
print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
print(f"Allocated GPU Memory: {torch.cuda.memory_allocated(device)}")
print(f"Reserved GPU Memory: {torch.cuda.memory_reserved(device)}")
model.to(device)
model.eval()

print("Model loaded successfully!")


def gemma_generate(prompt, max_tokens=10, temperature=0.2, top_p=0.5):
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Debugging: Print tokenized input IDs
    print(f"\n[DEBUG] Tokenized Input IDs: {inputs['input_ids']}\n")

    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id  
        )

    print(f"Generated Raw Tokens: {outputs}")  # Debugging

    # Extract only the generated tokens, removing input prompt
    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    print(f"Generated Response: {repr(response)}")  # Debugging

    return response.strip()

# Example test
if __name__ == "__main__":
    prompt = (
        "Answer the following mathematical question.\n"
        "Provide only the final number as the answer. Do not explain anything.\n"
        "Question: I have two apples. I get another apple. How many apples do I have now?\n"
        "Answer: "
    )
    
    response = gemma_generate(prompt, max_tokens=10, temperature=0.2, top_p=0.5)
    print(f"Model Response: {response}")

















    #def gemma_generate(prompt, max_tokens=100, temperature=0.7, top_p=0.9):
#    """
#    Generates text using Gemma 2-9B.
#
#    Args:
#        prompt (str): The input prompt.
#        max_tokens (int): Maximum number of tokens to generate.
#        temperature (float): Sampling temperature for diversity.
#        top_p (float): Top-p (nucleus) sampling for diversity.
#
#    Returns:
#        str: Generated text.
#    """
#    inputs = tokenizer(prompt, return_tensors="pt").to(device)
#
#    # Debugging: Print tokenized input IDs
#    print(f"Tokenized input IDs: {inputs['input_ids']}")
#
#    with torch.no_grad():
#        outputs = model.generate(
#            input_ids=inputs["input_ids"],
#            attention_mask=inputs["attention_mask"],
#            max_new_tokens=max_tokens,
#            temperature=temperature,
#            top_p=top_p,
#            do_sample=False  # Ensures a deterministic output
#        )
#
#    # Extract only the generated tokens, removing input prompt
#    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
#    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
#
#    return response.strip()  # Remove trailing spaces/newlines
