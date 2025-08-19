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
        
        Args:
            image_path (str): The file path for the medical image.
            patient_notes (str): Text notes from the patient or doctor.

        Returns:
            str: The final generated diagnosis.
        """
        # Open the image file
        raw_image = Image.open(image_path).convert("RGB")
        
        # Formulate a direct question to the VQA model
        question = "What disease or medical condition is visible in this image?"
        
        # Get a direct analysis from the VQA model
        image_analysis = self.vlm.get_visual_answer(raw_image, question)

        # Create a more effective, detailed prompt for the LLM
        prompt = (
            "You are a medical diagnosis assistant. Based on the following information, "
            "provide a potential diagnosis. Be cautious and recommend consulting a human specialist.\n\n"
            f"Patient Notes: \"{patient_notes}\"\n\n"
            f"Image Analysis Result: \"{image_analysis}\"\n\n"
            "Potential Diagnosis and Recommendations:"
        )

        # Generate the final diagnosis from the LLM
        final_diagnosis = self.llm.generate_diagnosis(prompt)

        return final_diagnosis