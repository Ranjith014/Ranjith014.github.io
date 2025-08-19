import gradio as gr
import requests

def get_diagnosis(image, patient_notes):
    """
    Function to call the FastAPI backend.
    """
    files = {'image': ("image.jpg", image, 'image/jpeg')}
    data = {'patient_notes': patient_notes}
    response = requests.post("http://127.0.0.1:8000/diagnose/", files=files, data=data)
    return response.json()["diagnosis"]

iface = gr.Interface(
    fn=get_diagnosis,
    inputs=[gr.Image(type="filepath"), gr.Textbox(lines=5, label="Patient Notes")],
    outputs="text",
    title="MedPredict: Disease Diagnosis Assistant",
    description="Upload a medical image and enter patient notes to get a potential diagnosis."
)

if __name__ == "__main__":
    iface.launch()