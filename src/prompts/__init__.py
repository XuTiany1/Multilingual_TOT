import importlib

def load_mgsm_module(lang: str):
    """
    Dynamically load the MGSM module based on language code (e.g., 'BN', 'EN', 'SW').
    
    Usage:
        mgsm = load_mgsm_module('EN')
        print(mgsm.standard_prompt)
    """
    module_name = f"src.prompts.MGSM_{lang.upper()}"  # Ensure case consistency
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(f"Language module 'MGSM_{lang.upper()}' not found in src/prompts/")