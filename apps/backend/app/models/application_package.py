import os
from google import genai
from google.genai import types
from pydantic import BaseModel

# Import your models
# (Assuming these are in the structure we discussed previously)
from models.user_profile import UserProfile
from models.job_requirement import JobRequirement
from models.alignment import AlignmentAnalysis

class AlignmentEngine:
    def __init__(self, api_key: str = None):
        """
        Initialize the Gemini Client. 
        Best practice: Load API key from environment variables.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        self.client = genai.Client(api_key=self.api_key)
        
        # Use Gemini 2.0 Flash for speed/cost, or Pro for complex reasoning
        self.model_name = "gemini-2.0-flash" 

    def analyze_fit(self, user: UserProfile, job: JobRequirement) -> AlignmentAnalysis:
        """
        The Core Porting Logic:
        1. Serializes domain objects to text.
        2. Configures Gemini to enforce the 'AlignmentAnalysis' Pydantic schema.
        3. Returns the strictly typed object.
        """

        # 1. Construct the Prompt
        # We dump the Pydantic models to JSON strings to give the LLM clear context
        prompt = f"""
        You are a Career Strategy AI. Your goal is to analyze the fit between a candidate and a job.
        
        ### CANDIDATE PROFILE (JSON):
        {user.model_dump_json()}

        ### JOB REQUIREMENT (JSON):
        {job.model_dump_json()}

        ### INSTRUCTIONS:
        1. Compare the candidate's experience specifically against the job's 'top_attributes'.
        2. For each attribute, determine if there is a gap (NONE, PARTIAL, MISSING).
        3. Provide a 'suggested_fix' for every row.
        4. Assign a score (0-100) based on the evidence.
        
        Output strictly in the JSON schema provided.
        """

        # 2. Call Gemini with Structured Output (The Magic Part)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", 
                response_schema=AlignmentAnalysis, # <--- Pass your Pydantic class here!
                temperature=0.1 # Keep it low for factual analysis
            )
        )

        # 3. Return the parsed object
        # The SDK automatically validates the JSON against your class
        # If the LLM output is invalid, this will raise a Pydantic ValidationError
        return response.parsed