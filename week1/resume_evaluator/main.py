import asyncio
import json
import os
import re
from io import BytesIO
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from groq import AsyncGroq
from pypdf import PdfReader

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")

client = AsyncGroq(api_key=GROQ_API_KEY)
MODEL = "openai/gpt-oss-120b"

app = FastAPI(title="AI Resume Evaluator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True) 
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def parse_llm_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    return json.loads(cleaned)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Server error: {str(exc)}"},
    )


def extract_pdf_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    return text[:14000]


def derive_verdict(score: int) -> str:
    if score >= 85:
        return "Strong Fit"
    if score >= 70:
        return "Good Match"
    if score >= 50:
        return "Partial Match"
    return "Low Fit"


async def evaluate_resume(
    jd_text: str, filename: str, pdf_bytes: bytes, semaphore: asyncio.Semaphore
) -> dict:
    resume_text = extract_pdf_text(pdf_bytes)
    base_name = filename.rsplit(".", 1)[0]

    if not resume_text:
        return {
            "file_name": filename,
            "candidate_name": base_name,
            "score": 0,
            "verdict": "Low Fit",
            "summary": "No extractable text found in PDF (may be a scanned or image-based PDF).",
            "matched_skills": [],
            "missing_skills": [],
            "key_takeaways": ["Upload a text-selectable PDF resume for accurate parsing."],
        }

    system_prompt = (
        "You are an objective technical recruiter and resume scorer. "
        "Compare the candidate's resume against the job description (JD). "
        "Return ONLY valid JSON with exact keys:\n"
        "{\n"
        '  "candidate_name": "string",\n'
        '  "score": integer (0 to 100),\n'
        '  "verdict": "Strong Fit" | "Good Match" | "Partial Match" | "Low Fit",\n'
        '  "summary": "2-3 sentence evaluation",\n'
        '  "matched_skills": ["string"],\n'
        '  "missing_skills": ["string"],\n'
        '  "key_takeaways": ["string"]\n'
        "}"
    )

    async with semaphore:
        completion = await client.chat.completions.create(
            model=MODEL,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"JOB DESCRIPTION:\n{jd_text}\n\nRESUME FILE ({filename}):\n{resume_text}",
                },
            ],
        )

    raw = completion.choices[0].message.content or "{}"
    try:
        data = parse_llm_json(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned invalid JSON: {exc}. Raw output: {raw[:300]}")

    score = max(0, min(100, int(data.get("score", 0))))
    verdict = data.get("verdict") or derive_verdict(score)

    return {
        "file_name": filename,
        "candidate_name": data.get("candidate_name") or base_name,
        "score": score,
        "verdict": verdict,
        "summary": data.get("summary") or "",
        "matched_skills": data.get("matched_skills") or [],
        "missing_skills": data.get("missing_skills") or [],
        "key_takeaways": data.get("key_takeaways") or [],
    }


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/candidate/evaluate")
async def candidate_evaluate(
    jd_text: str = Form(...),
    resume: UploadFile = File(...),
):
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")

    pdf_bytes = await resume.read()
    semaphore = asyncio.Semaphore(1)
    result = await evaluate_resume(jd_text.strip(), resume.filename, pdf_bytes, semaphore)
    return result


@app.post("/api/hr/rank")
async def hr_rank(
    jd_text: str = Form(...),
    top_n: str = Form("10"),
    resumes: List[UploadFile] = File(...),
):
    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    pdf_files = [
        f for f in resumes if f.filename and f.filename.lower().endswith(".pdf")
    ]
    if not pdf_files:
        raise HTTPException(status_code=400, detail="Please upload at least one PDF resume.")

    loaded_resumes = []
    for f in pdf_files:
        content = await f.read()
        loaded_resumes.append((f.filename, content))

    semaphore = asyncio.Semaphore(4)
    tasks = [
        evaluate_resume(jd_text.strip(), name, data, semaphore)
        for name, data in loaded_resumes
    ]
    scored = await asyncio.gather(*tasks)

    ranked = sorted(scored, key=lambda item: item["score"], reverse=True)

    if top_n.lower() == "all":
        limit_count = len(ranked)
    else:
        try:
            limit_count = max(1, min(len(ranked), int(top_n)))
        except ValueError:
            limit_count = min(10, len(ranked))

    return {
        "total_processed": len(ranked),
        "shortlist_count": limit_count,
        "shortlist": ranked[:limit_count],
        "all_ranked": ranked,
    }