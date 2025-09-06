import io
import base64
from PIL import Image
import PyPDF2
from typing import Union
import google.generativeai as genai
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize APIs (you'll need to set these environment variables)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_image(image_data: bytes) -> str:
    """Extract text from image using Gemini 1.5 Flash"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        image = Image.open(io.BytesIO(image_data))
        prompt = "Extract all text from this medical claim document. Return only the raw text without any formatting:"
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        raise Exception(f"Image text extraction failed: {str(e)}")

def extract_text_from_pdf(pdf_data: bytes) -> str:
    """Extract text from PDF"""
    try:
        pdf_file = io.BytesIO(pdf_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        print(text)
        
        return text
    except Exception as e:
        raise Exception(f"PDF text extraction failed: {str(e)}")


def extract_structured_data(text: str) -> dict:
    """Extract structured data from text using Gemini 1.5 Flash"""
    prompt = f"""
    Extract medical claim information from the following text and return ONLY valid JSON in this exact structure:

    {{
        "patient": {{
            "name": "string or null",
            "age": "number or null"
        }},
        "diagnoses": ["array of strings"],
        "medications": [
            {{
                "name": "string or null",
                "dosage": "string or null", 
                "quantity": "string or null"
            }}
        ],
        "procedures": ["array of strings"],
        "admission": {{
            "was_admitted": "boolean",
            "admission_date": "string or null in YYYY-MM-DD format",
            "discharge_date": "string or null in YYYY-MM-DD format"
        }},
        "total_amount": "string or null"
    }}

    Text to analyze:
    {text}
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        print(response.text)
        return response.text  # You may want to parse this as JSON before returning
    except Exception as e:
        raise Exception(f"Structured extraction failed: {str(e)}")
    

def answer_question(document_text: str, question: str) -> str:
    """Answer questions about the document using Gemini 1.5 Flash"""
    prompt = f"""
    Based on the following medical claim document text, answer this question: {question}
    
    Document text:
    {document_text}
    
    Return only the direct answer without any additional text or explanation.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Question answering failed: {str(e)}")