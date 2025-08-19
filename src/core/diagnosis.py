# src/core/diagnosis.py (Final Corrected Version)

from src.core.models import VLM, LLM
from PIL import Image

class DiagnosisAssistant:
    def __init__(self):
        """
        Initializes the assistant with the VQA and LLM models.
        """
        self.vlm = VLM()
        self.llm = LLM()

    def diagnose(self, image_path, patient_notes):
        """
        Performs a multimodal diagnosis using Visual Question Answering.
        """
        raw_image = Image.open(image_path).convert("RGB")
        question = "What medical condition is visible in this image?"
        image_analysis = self.vlm.get_visual_answer(raw_image, question)

        # --- THIS IS THE FINAL FIX: A MUCH BETTER PROMPT ---
        # This new prompt structure is clearer for a simple model like GPT-2.
        # It uses strong separators and a leading phrase to force the AI to generate a diagnosis.
        prompt = (
            "### INSTRUCTIONS ###\n"
            "You are a medical diagnosis assistant. Analyze the following clinical information and provide a potential diagnosis. Conclude by strongly recommending consultation with a human specialist.\n\n"
            "### CLINICAL INFORMATION ###\n"
            f"- Patient Notes: {patient_notes}\n"
            f"- Radiology Finding from Image: {image_analysis}\n\n"
            "### POTENTIAL DIAGNOSIS ###\n"
            "Based on the clinical information provided, the potential diagnosis is a" # The AI will complete this sentence.
        )

        final_diagnosis = self.llm.generate_diagnosis(prompt)

        return final_diagnosis