import importlib
import os

# Automatically detect available MGSM modules
PROMPT_DIR = os.path.dirname(__file__)  # Get directory of this file
AVAILABLE_LANGUAGES = {
    f.split("MGSM_")[1].split(".py")[0].upper()
    for f in os.listdir(PROMPT_DIR)
    if f.startswith("MGSM_") and f.endswith(".py")
}

def load_mgsm_module(lang: str):
    """
    Dynamically load the MGSM module based on the language code (e.g., 'BN', 'EN', 'SW').

    Usage:
        mgsm = load_mgsm_module('EN')
        print(mgsm.standard_prompt)
    """
    lang = lang.upper()
    
    if lang not in AVAILABLE_LANGUAGES:
        raise ValueError(
            f"Language module 'MGSM_{lang}' not found in src/prompts/.\n"
            f"Available languages: {sorted(AVAILABLE_LANGUAGES)}"
        )
    
    module_name = f"src.prompts.MGSM_{lang}"
    
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ImportError(f"Could not import '{module_name}'. Check if the file exists and is correctly named.")