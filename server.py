import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

# Load environment variables
load_dotenv()

app = FastAPI(title="Movie Information Extraction Bot")

# Base directory for static files
BASE_DIR = Path(__file__).resolve().parent

SYSTEM_PROMPT = """You are a highly accurate information extraction assistant.

Your task is to analyze a paragraph about a movie and extract useful,
structured information from it.

IMPORTANT:
You are an INFORMATION EXTRACTION system, not a movie knowledge system.

You MUST use ONLY the information explicitly stated in the provided paragraph.

DO NOT:
- Use your existing knowledge about movies.
- Guess the movie name.
- Guess actors or actresses.
- Guess the director.
- Guess the release year.
- Guess character names.
- Identify a movie based on clues.
- Add information that is not present in the paragraph.
- Treat logical assumptions as facts.

If a field cannot be determined from the paragraph, write:
"Not mentioned"

OUTPUT FORMAT:
Return the result using exactly this format:

Movie Name: ...
Genre: ...
Cast: ...
Director: ...
Release Year: ...
Main Characters: ...
Plot: ...
Themes: ...
Setting: ...
Important Keywords: ...
Quick Summary: ...

Do not add an introduction.
Do not add an explanation.
Do not add information outside these fields."""

class ExtractRequest(BaseModel):
    paragraph: str

@app.post("/extract")
@app.post("/api/extract")
@app.post("/api/index")
async def extract_info(req: ExtractRequest):
    if not req.paragraph or not req.paragraph.strip():
        raise HTTPException(status_code=400, detail="Paragraph cannot be empty.")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is missing.")

    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze the following movie paragraph and extract the information according to the rules provided above.\n\nPARAGRAPH:\n{req.paragraph}"}
            ],
            temperature=0.2
        )
        return {"result": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def serve_index():
    return FileResponse(BASE_DIR / "index.html")

# Serve static assets (style.css, script.js, etc.)
app.mount("/", StaticFiles(directory=str(BASE_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
