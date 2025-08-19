# main.py (Final Corrected Version)

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os

# 1. --- THIS IMPORT WAS MISSING ---
# This line imports the class that does the actual work.
# Make sure your diagnosis logic is in 'src/core/diagnosis.py'
from src.core.diagnosis import DiagnosisAssistant

# --- THIS IS THE FIX ---
# Create an instance of the FastAPI application.
app = FastAPI()

# 2. --- THIS INSTANCE CREATION WAS MISSING ---
# We create one instance of the assistant when the server starts.
# This object will be used for all incoming requests.
try:
    print("--> Preparing to initialize DiagnosisAssistant...")
    diagnosis_assistant = DiagnosisAssistant()
    print("--> DiagnosisAssistant initialized successfully. Server is ready for requests.")
except Exception as e:
    # If the model fails to load, the server will still run but endpoints will report an error.
    print(f"FATAL: Could not initialize DiagnosisAssistant. Error: {e}")
    diagnosis_assistant = None


@app.post("/diagnose/")
async def diagnose(file: UploadFile = File(...), patient_notes: str = Form(...)):
    # Check if the assistant was loaded correctly on startup
    if diagnosis_assistant is None:
        raise HTTPException(status_code=500, detail="Diagnosis Assistant is not available due to a server initialization error. Check the backend logs.")

    temp_path = "temp_image.jpg"
    
    try:
        # Save the uploaded image
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Now, this call will work because 'diagnosis_assistant' is defined
        diagnosis = diagnosis_assistant.diagnose(temp_path, patient_notes)
        
        return {"diagnosis": diagnosis}

    except Exception as e:
        # Log the detailed error to the backend terminal
        print(f"An error occurred during diagnosis: {e}")
        # Return a generic error to the frontend
        raise HTTPException(status_code=500, detail=f"An internal error occurred during diagnosis.")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)