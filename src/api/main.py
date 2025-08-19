# --- ENHANCED main.py with logging ---
import os
from fastapi import FastAPI, File, UploadFile, Form
from src.core.diagnosis import DiagnosisAssistant
import time
import datetime

app = FastAPI()

print("--> Preparing to initialize DiagnosisAssistant...")
diagnosis_assistant = DiagnosisAssistant()
print("--> DiagnosisAssistant initialized successfully. Server is ready for requests.")

@app.post("/diagnose/")
async def diagnose(image: UploadFile = File(...), patient_notes: str = Form(...)):
    """
    API endpoint to get a diagnosis from an image and text.
    """
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{request_time}] -----------------------------------------")
    print(f"[{request_time}] ✅ Request received for image: {image.filename}")
    
    # Define a temporary path to save the uploaded image
    image_path = f"temp_{image.filename}"
    
    try:
        # Save the uploaded image to the temporary path
        with open(image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        print(f"[{request_time}] ➡️ Image saved to temporary file: {image_path}")

        # Get diagnosis from the core assistant
        print(f"[{request_time}] 🧠 Calling the AI diagnosis assistant... (This may take a moment on CPU)")
        start_time = time.time()
        diagnosis = diagnosis_assistant.diagnose(image_path, patient_notes)
        end_time = time.time()
        print(f"[{request_time}] ✨ AI diagnosis finished in {end_time - start_time:.2f} seconds.")

    finally:
        # Ensure the temporary file is deleted after diagnosis
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"[{request_time}] 🗑️ Temporary file deleted.")

    print(f"[{request_time}] 🚀 Sending diagnosis back to the user.")
    print(f"[{request_time}] -----------------------------------------\n")
    return {"diagnosis": diagnosis}