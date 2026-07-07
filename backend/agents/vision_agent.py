import os
import base64
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

def _get_model():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("WARNING: GROQ_API_KEY not set.")
    return ChatGroq(model="llama-3.2-11b-vision-preview", groq_api_key=api_key)

def analyze_complaint_image(image_data: bytes, mime_type: str) -> dict:
    """Uses Groq Vision to analyze an image for civic complaints (potholes, garbage, etc.)"""
    model = _get_model()
    prompt = "Analyze this image. Does it show a civic issue like a pothole, garbage, broken streetlight, or water leak? Respond with a JSON object containing keys: 'category' (e.g. 'Pothole', 'Garbage'), 'description' (a short description of the issue), 'priority' (High/Medium/Low)."
    
    base64_image = base64.b64encode(image_data).decode("utf-8")
    
    try:
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                },
            ]
        )
        response = model.invoke([message])
        return {
            "status": "success",
            "raw_analysis": response.content
        }
    except Exception as e:
        print(f"Error in analyze_complaint_image: {e}")
        return {"status": "error", "message": str(e)}

def extract_document_ocr(image_data: bytes, mime_type: str) -> dict:
    """Uses Groq Vision to perform OCR and verification on official documents (e.g. Aadhaar)."""
    model = _get_model()
    prompt = "Analyze this government ID document. Extract the following information as JSON: 'name', 'dob', 'id_number', 'document_type' (e.g. Aadhaar, PAN, Driving License), 'is_valid' (boolean, is it a clear legible document or blurry/fake)."
    
    base64_image = base64.b64encode(image_data).decode("utf-8")
    
    try:
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                },
            ]
        )
        response = model.invoke([message])
        return {
            "status": "success",
            "extracted_data": response.content
        }
    except Exception as e:
        print(f"Error in extract_document_ocr: {e}")
        return {"status": "error", "message": str(e)}
