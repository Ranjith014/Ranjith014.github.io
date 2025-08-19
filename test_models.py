# test_models.py
from transformers import BlipProcessor, BlipForQuestionAnswering, GPT2Tokenizer, GPT2LMHeadModel
import torch # It's good practice to import torch to check the installation

print("--- Step 1: Testing PyTorch installation ---")
print(f"PyTorch version: {torch.__version__}")
print("PyTorch installation looks OK.")
print("\n---------------------------------------------------\n")

try:
    # --- Test VLM (BLIP) Model ---
    print("--- Step 2: Testing VLM (BLIP) model loading ---")
    print("Attempting to download/load Salesforce/blip-vqa-base...")
    vlm_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
    vlm_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
    print("SUCCESS: VLM (BLIP) model and processor loaded correctly.")
    print("\n---------------------------------------------------\n")

    # --- Test LLM (GPT-2) Model ---
    print("--- Step 3: Testing LLM (GPT-2) model loading ---")
    print("Attempting to download/load gpt2...")
    llm_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    llm_model = GPT2LMHeadModel.from_pretrained("gpt2")
    print("SUCCESS: LLM (GPT-2) model and tokenizer loaded correctly.")
    print("\n---------------------------------------------------\n")

    print("✅ ALL TESTS PASSED! Your environment is ready to run the application.")

except Exception as e:
    print("\n❌ AN ERROR OCCURRED! ❌")
    print("The application cannot run because a model failed to load.")
    print(f"Error details: {e}")