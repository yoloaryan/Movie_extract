import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Try loading .env if running in an environment with local .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Movie Information Extraction Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Extraction Prompt
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a highly accurate information extraction assistant.

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
Do not add information outside these fields.
"""
    ),
    (
        "human",
        """
Analyze the following movie paragraph and extract the information
according to the rules provided above.

PARAGRAPH:
{paragraph}
"""
    )
])

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
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY environment variable is missing. Please configure it in Vercel project settings."
        )

    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    try:
        model = ChatGroq(
            model=model_name,
            temperature=0.2,
            api_key=api_key
        )
        final_prompt = prompt_template.invoke({"paragraph": req.paragraph})
        response = model.invoke(final_prompt)
        return {"result": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
