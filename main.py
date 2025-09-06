from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import uuid
import json
from models import DocumentUpload, QuestionRequest, QuestionResponse, ExtractionResponse
from utils import extract_text_from_image, extract_text_from_pdf, extract_structured_data, answer_question
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Intelligent Claims QA")

# In-memory storage
documents_store: Dict[str, dict] = {}

@app.post("/extract", response_model=ExtractionResponse)
async def extract_claim_data(file: UploadFile = File(...)):
    """
    Extract structured data from medical claim documents (image or PDF)
    """
    try:

        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        if file.content_type.startswith('image/'):
            extracted_text = extract_text_from_image(file_content)
        elif file.content_type == 'application/pdf':
            extracted_text = extract_text_from_pdf(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Extract structured data
        structured_data_json = extract_structured_data(extracted_text)
        
        # Parse JSON response
        try:
            structured_data = json.loads(structured_data_json)
        except json.JSONDecodeError:
            # Clean up potential markdown code blocks
            cleaned_json = structured_data_json.strip().replace('```json', '').replace('```', '')
            structured_data = json.loads(cleaned_json)
        
        # Generate unique document ID and store
        document_id = str(uuid.uuid4())
        documents_store[document_id] = {
            "text": extracted_text,
            "structured_data": structured_data
        }
        
        # Add document_id to response
        response_data = structured_data.copy()
        response_data["document_id"] = document_id
        print(document_id)
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer questions about a previously processed document
    """
    try:
        # Retrieve document from storage
        if request.document_id not in documents_store:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document_data = documents_store[request.document_id]
        document_text = document_data["text"]
        
        # Answer the question
        answer = answer_question(document_text, request.question)
        
        return QuestionResponse(answer=answer)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question answering failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "documents_stored": len(documents_store)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)