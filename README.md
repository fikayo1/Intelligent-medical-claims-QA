# Intelligent Claims QA

This project provides an API service for extracting structured data from medical claim documents (PDFs or images) and answering questions about them using Google Gemini 1.5 Flash. The service is built with FastAPI and leverages generative AI for both text extraction and question answering.

---

## Approach

- **Text Extraction:**  
  - For images, the service uses Gemini 1.5 Flash to extract raw text directly from the image.
  - For PDFs, it uses PyPDF2 to extract text from each page.
- **Structured Data Extraction:**  
  - The extracted text is sent to Gemini 1.5 Flash with a prompt requesting a specific JSON structure for medical claims.
- **Question Answering:**  
  - Users can ask questions about previously processed documents. The service uses Gemini 1.5 Flash to answer based on the stored document text.
- **Storage:**  
  - Documents and their structured data are stored in-memory using a Python dictionary, keyed by a UUID.
- **API Endpoints:**  
  - `/extract`: Upload a document and receive structured data plus a document ID.
  - `/ask`: Ask a question about a previously processed document using its ID.
  - `/health`: Health check endpoint.

---

## Assumptions & Decisions

- **Gemini 1.5 Flash is used for all AI tasks** (text extraction from images, structured data extraction, and question answering) for cost efficiency and simplicity.
- **PDF text extraction uses PyPDF2** for reliability and speed.
- **In-memory storage** is used for simplicity; this is not persistent and is suitable only for local/demo use.
- **Environment variables** are used for API keys (`GEMINI_API_KEY` and `OPENAI_API_KEY`), loaded via `python-dotenv`.
- **Error handling** is implemented for file type validation, JSON parsing, and AI service failures.
- **No authentication** is implemented; this is intended for local or internal use.

---

## Running Locally

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd curacel
```

### 2. Install Dependencies

Make sure you have Python 3.9+ installed.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**Sample `requirements.txt`:**
```
fastapi
uvicorn
python-dotenv
PyPDF2
Pillow
google-generativeai
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Only needed if you use OpenAI elsewhere
```

### 4. Run the Service

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## API Usage

### `/extract` (POST)

Upload a PDF or image file.  
**Returns:** Structured claim data and a `document_id`.

**Example with `curl`:**
```bash
curl -F "file=@claim.pdf" http://localhost:8000/extract
```

### `/ask` (POST)

Ask a question about a previously processed document.

**Request JSON:**
```json
{
  "document_id": "your-document-id",
  "question": "What is the total amount claimed?"
}
```

### `/health` (GET)

Check service health and number of stored documents.

---

## Notes

- Gemini API usage may have quotas or rate limits.
- If Gemini returns JSON in a code block, the service will attempt to clean and parse it.

---