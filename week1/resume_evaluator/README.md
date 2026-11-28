# AI Resume Evaluator

An AI-powered resume screening and ranking application built using **FastAPI, Groq LLM, and Python**. It evaluates candidate resumes against a given Job Description (JD), identifies relevant and missing skills, generates an evaluation summary, and ranks multiple candidates based on their suitability.

## 1. Project Overview

The application provides two primary workflows:

- **Candidate Evaluation:** Evaluates an individual resume against a Job Description and generates a suitability score with detailed feedback.
- **HR Resume Ranking:** Processes multiple PDF resumes concurrently, evaluates each candidate, and generates a ranked shortlist based on their scores.

The application uses Groq's LLM API (`openai/gpt-oss-120b`) to perform AI-based resume analysis.

## 2. Key Features

- PDF resume text extraction using PyPDF.
- AI-based resume and Job Description comparison.
- Candidate suitability scoring (0–100).
- Automatic candidate-fit classification.
- Matched and missing skills identification.
- AI-generated evaluation summaries and key takeaways.
- Concurrent processing of multiple resumes.
- Candidate ranking and customizable shortlisting.
- JSON-formatted AI responses.
- REST API implementation using FastAPI.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API and application framework |
| Groq API | LLM-powered resume evaluation |
| GPT-OSS-120B | Resume analysis model |
| PyPDF | PDF text extraction |
| AsyncGroq | Asynchronous LLM requests |
| python-dotenv | Environment variable management |
| asyncio | Concurrent task execution |
| StaticFiles | Frontend static file serving |

## 4. Application Architecture

The application follows this processing workflow:

**Resume Upload → PDF Text Extraction → Job Description Comparison → Groq LLM Analysis → JSON Processing → Score Generation → Candidate Evaluation / Ranking**

### Main Components

**1. Configuration and Initialization**
- Loads environment variables using `python-dotenv`.
- Initializes the asynchronous Groq client.
- Configures the FastAPI application.
- Enables CORS middleware.
- Mounts the static directory for frontend resources.

**2. PDF Processing**
- Reads uploaded PDF files into memory.
- Extracts text from individual PDF pages using `PdfReader`.
- Limits extracted resume text to 14,000 characters.

**3. AI Evaluation Engine**
- Sends the Job Description and extracted resume text to the Groq model.
- Uses a structured system prompt to obtain consistent evaluation results.
- Requests JSON-formatted responses.
- Extracts candidate details, skills, score, summary, and recommendations.

**4. Scoring and Verdict Generation**

The application uses the following suitability categories:

| Score | Verdict |
|---|---|
| 85–100 | Strong Fit |
| 70–84 | Good Match |
| 50–69 | Partial Match |
| 0–49 | Low Fit |

**5. HR Ranking Engine**
- Processes multiple uploaded resumes.
- Uses an asynchronous semaphore to limit concurrent evaluations to four.
- Sorts candidates in descending order of their scores.
- Generates a shortlist based on the requested `top_n` value.

## 5. Important Functions

| Function | Responsibility |
|---|---|
| `parse_llm_json()` | Cleans and parses the LLM-generated JSON response. |
| `extract_pdf_text()` | Extracts text from uploaded PDF resumes. |
| `derive_verdict()` | Determines the candidate-fit category from the score. |
| `evaluate_resume()` | Core evaluation engine that compares resume content with the JD using Groq. |
| `candidate_evaluate()` | Handles individual candidate evaluation requests. |
| `hr_rank()` | Evaluates, sorts, and shortlists multiple candidates. |
| `home()` | Serves the frontend HTML page. |

## 6. API Documentation

### A. Individual Candidate Evaluation

**Endpoint:** `POST /api/candidate/evaluate`

Evaluates one candidate's resume against a Job Description.

**Request Content Type:** `multipart/form-data`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `jd_text` | String | Yes | Job Description text |
| `resume` | PDF File | Yes | Candidate resume |

**Example Response:**

```json
{
  "file_name": "candidate.pdf",
  "candidate_name": "John Doe",
  "score": 88,
  "verdict": "Strong Fit",
  "summary": "The candidate demonstrates strong technical alignment with the job requirements.",
  "matched_skills": ["Python", "FastAPI", "SQL"],
  "missing_skills": ["AWS"],
  "key_takeaways": [
    "Strong backend development experience",
    "Relevant API development knowledge"
  ]
}
```

### B. HR Resume Ranking

**Endpoint:** `POST /api/hr/rank`

Evaluates multiple candidate resumes and returns a ranked candidate list.

**Request Content Type:** `multipart/form-data`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `jd_text` | String | Yes | Job Description text |
| `resumes` | PDF Files | Yes | Multiple candidate resumes |
| `top_n` | String | No | Number of candidates to shortlist; defaults to 10 |

**Supported `top_n` Values:**
- `5` – Top 5 candidates.
- `10` – Top 10 candidates.
- `all` – All evaluated candidates.

**Example Response:**

```json
{
  "total_processed": 3,
  "shortlist_count": 2,
  "shortlist": [
    {
      "file_name": "candidate1.pdf",
      "candidate_name": "John",
      "score": 92,
      "verdict": "Strong Fit",
      "summary": "Strong alignment with the job requirements.",
      "matched_skills": ["Python", "FastAPI"],
      "missing_skills": ["Docker"],
      "key_takeaways": ["Strong backend experience"]
    }
  ],
  "all_ranked": []
}
```

*Note: Response values above are illustrative.*

## 7. Project Structure

```text
AI-Resume-Evaluator/
│
├── main.py                 # FastAPI backend and evaluation logic
│
├── static/
│   ├── index.html          # Frontend entry point
│   ├── style.css           # Frontend styling (if present)
│   └── script.js           # Frontend logic (if present)
│
├── .env                    # Groq API credentials
├── .gitignore              # Git ignored files
└── requirements.txt        # Python dependencies
```

*The structure represents the expected project organization; optional frontend files should be included if they exist in your project.*

## 8. Installation and Setup

### Prerequisites

- Python 3.10+
- Groq API key
- pip package manager

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd AI-Resume-Evaluator
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install fastapi uvicorn python-multipart python-dotenv groq pypdf
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit the `.env` file to version control.

### Step 5: Run the Application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

### Step 6: Access API Documentation

FastAPI automatically provides interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 9. Concurrency and Performance

The application uses Python's asynchronous programming capabilities to improve processing efficiency.

- Individual evaluation uses a semaphore limit of 1.
- HR ranking allows up to 4 simultaneous resume evaluations.
- `asyncio.gather()` coordinates multiple evaluation tasks.
- LLM requests are handled asynchronously through `AsyncGroq`.

This approach reduces sequential waiting during bulk resume screening while controlling the number of concurrent LLM requests.

## 10. Error Handling and Validation

The application implements the following validations:

- Checks whether the Groq API key exists.
- Rejects empty Job Descriptions.
- Validates PDF file extensions.
- Rejects requests without valid PDF resumes.
- Handles JSON parsing failures.
- Returns HTTP 400 for invalid user input.
- Returns HTTP 500 for unhandled server errors.

**PDF Limitation:** Scanned or image-based PDFs may not produce extractable text. The application currently does not implement OCR.

## 11. Future Improvements

- Add OCR support for scanned PDF resumes.
- Implement file-size and upload-count restrictions.
- Add stronger PDF content validation.
- Introduce structured logging and improved exception handling.
- Add authentication and role-based access for HR users.
- Improve ranking with configurable evaluation criteria.
- Add persistent storage for candidate evaluation history.
- Implement stricter validation of AI-generated JSON fields.

---

**Project:** AI Resume Evaluator  
**Backend:** FastAPI  
**AI Provider:** Groq  
**Model:** openai/gpt-oss-120b  
**Primary Purpose:** Automated Resume Evaluation and Candidate Ranking