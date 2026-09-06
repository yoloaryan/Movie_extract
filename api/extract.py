import os
import json
from http.server import BaseHTTPRequestHandler

# Try loading .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SYSTEM_PROMPT = """You are a highly accurate information extraction assistant.

Your task is to analyze a paragraph about a movie and extract useful, structured information from it.

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

class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        response = {
            "status": "online",
            "message": "Movie Information Extraction API is running."
        }
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON format."}).encode("utf-8"))
            return

        paragraph = body.get("paragraph", "").strip()
        if not paragraph:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Paragraph cannot be empty."}).encode("utf-8"))
            return

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "GROQ_API_KEY environment variable is missing. Please add it in your Vercel project Settings -> Environment Variables."
            }).encode("utf-8"))
            return

        model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze the following movie paragraph and extract the information according to the rules provided above.\n\nPARAGRAPH:\n{paragraph}"}
                ],
                temperature=0.2
            )
            result_text = completion.choices[0].message.content

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"result": result_text}).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
