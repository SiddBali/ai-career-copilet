# pyrefly: ignore [missing-import]
from google import genai
from pydantic import BaseModel
from typing import List
import json


class ResumeAnalysis(BaseModel):
    skills: List[str]
    missing_skills: List[str]
    roadmap: List[str]
    interview_questions: List[str]


def analyze_resume(resume_text, user_goal):
    try:
        client = genai.Client()
        prompt = f"""
You are the senior software engineer and hiring manager.

Evaluate the resume based on the user's goal. 

User goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skills for this goal.
- REMOVE irrelevant tools (e.g. excel for backend, etc.).
- Identify real gaps.
- Generate roadmap only for the missing fields.
- Make the output DIFFERENT based on goal.

Resume:
{resume_text}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ResumeAnalysis,
                "temperature": 0.3,
                "system_instruction": "you are a strict hiring manager."
            }
        )
        return json.loads(response.text)

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }