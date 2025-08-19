# src/core/models.py (Complete Corrected File)

from transformers import BlipProcessor, BlipForQuestionAnswering, GPT2Tokenizer, GPT2LMHeadModel
import torch

class VLM:
    """
    Visual Language Model (BLIP) for answering questions about images.
    """
    def __init__(self):
        print("--> Initializing VLM (BLIP)...")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        self.model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        print("--> VLM (BLIP) initialized.")

    def get_visual_answer(self, image, question):
        """
        Generates an answer to a question based on an image.
        """
        inputs = self.processor(image, question, return_tensors="pt")
        out = self.model.generate(**inputs, max_new_tokens=50)
        answer = self.processor.decode(out[0], skip_special_tokens=True)
        return answer

class LLM:
    """
    Large Language Model (GPT-2) for generating text-based diagnoses.
    """
    def __init__(self):
        print("--> Initializing LLM (GPT-2)...")
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        # Add a padding token to handle batches of different lengths
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # --- THIS WAS THE BUG ---
        # The model was likely loaded into a local variable.
        # It MUST be saved to 'self.model' to be accessible by other methods.
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        print("--> LLM (GPT-2) initialized.")

    def generate_diagnosis(self, prompt):
        """
        Generates a detailed diagnosis based on a prompt.
        """
        # Encode the prompt into tokens
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
        
        # Generate text using the model
        # max_length can be adjusted to control the length of the output
        output_sequences = self.model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=200,  # Increased length for a more detailed response
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id 
        )
        
        # Decode the generated tokens back into a string
        generated_text = self.tokenizer.decode(output_sequences[0], skip_special_tokens=True)
        return generated_text