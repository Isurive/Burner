from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# DEPENDENCY NOTES:
# This model relies on data structures from:
# 1. models.user_profile (User experience data)
# 2. models.job_requirement (The "Top 6 Attributes" to align against)
# -----------------------------------------------------------------------------

# --- Enums for strict consistency (Frontend can use these for color coding) ---

class GapSeverity(str, Enum):
    NONE = "none"       # Green: Strong match found
    PARTIAL = "partial" # Yellow: Found, but weak or indirect
    MISSING = "missing" # Red: Not found in profile

class FixPriority(str, Enum):
    LOW = "low"         # Nice to have
    MEDIUM = "medium"   # Important for keywords
    HIGH = "high"       # Critical (Job requires this explicitly)

# --- Sub-Models ---

class AlignmentRow(BaseModel):
    """
    Represents a single row in the 'Gap Analysis' table.
    Maps a specific Job Attribute -> User Evidence.
    """
    attribute_name: str = Field(..., description="One of the top 6 attributes from JobRequirement")
    resume_evidence: Optional[str] = Field(None, description="Quote or summary of what was found in UserProfile")
    gap: GapSeverity
    suggested_fix: str = Field(..., description="Actionable advice: 'Add a bullet about X'")
    priority: FixPriority

class AlignmentScore(BaseModel):
    """
    Data point for the Radar Chart.
    """
    attribute_name: str
    score: int = Field(..., ge=0, le=100, description="0-100 match score")
    explanation: str = Field(..., description="1-sentence justification for the score")

# --- Main Model ---

class AlignmentAnalysis(BaseModel):
    """
    The Core Differentiator.
    This object is the result of comparing a UserProfile vs. a JobRequirement.
    """
    # Metadata
    job_id: str
    user_profile_id: str
    
    # 5.1 Alignment Map (The Table)
    alignment_rows: List[AlignmentRow]

    # 5.2 & 5.3 Scoring (The Radar Chart)
    # Validation: Ideally strictly 6 items, but List is flexible
    scores: List[AlignmentScore] 

    overall_match_percentage: int = Field(..., ge=0, le=100)

    class Config:
        schema_extra = {
            "example": {
                "job_id": "job_123",
                "user_profile_id": "user_456",
                "alignment_rows": [
                    {
                        "attribute_name": "Python Backend Dev",
                        "resume_evidence": "Worked with Django for 3 years",
                        "gap": "none",
                        "suggested_fix": "Highlight async optimization",
                        "priority": "low"
                    }
                ],
                "scores": [
                    {"attribute_name": "Python", "score": 90, "explanation": "Strong evidence found."}
                ],
                "overall_match_percentage": 85
            }
        }