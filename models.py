from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DocumentUpload(BaseModel):
    file: bytes

class QuestionRequest(BaseModel):
    document_id: str
    question: str

class QuestionResponse(BaseModel):
    answer: str

class PatientInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

class Medication(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    quantity: Optional[str] = None

class AdmissionInfo(BaseModel):
    was_admitted: bool = False
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None

class ExtractionResponse(BaseModel):
    patient: PatientInfo
    diagnoses: List[str]
    medications: List[Medication]
    procedures: List[str]
    admission: AdmissionInfo
    total_amount: Optional[str] = None