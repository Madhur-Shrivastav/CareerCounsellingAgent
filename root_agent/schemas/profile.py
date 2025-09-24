from typing import List, Literal
from pydantic import BaseModel, Field

class CareerPath(BaseModel):
    path: str = Field(..., description="Career title")
    match_percentage: int = Field(..., ge=0, le=100, description="0-100")

class ConfidenceIndicators(BaseModel):
    decision_making: Literal["High", "Medium", "Low"]
    self_awareness: Literal["High", "Medium", "Low"]
    exploration_readiness: Literal["High", "Medium", "Low"]

class InterestDistribution(BaseModel):
    STEM: int = Field(..., ge=0, le=100)
    Arts_Humanities: int = Field(..., ge=0, le=100)
    Business_Commerce: int = Field(..., ge=0, le=100)
    Social_Services: int = Field(..., ge=0, le=100)

class ProfileInAGist(BaseModel):
    subjects_good_at: List[str]
    natural_calling: str
    inclined_to_pursue: List[str]
    roadblocks: List[str]
    encouragement: str

class UserProfile(BaseModel):
    profile_summary: str
    identified_keywords: List[str]  # exactly 5
    primary_orientation: Literal["Analytical", "Creative", "Social", "Practical", "Investigative", "Enterprising"]
    orientation_confidence: int = Field(..., ge=0, le=100)

    analytical: int = Field(..., ge=0, le=100)
    creative: int = Field(..., ge=0, le=100)
    social: int = Field(..., ge=0, le=100)
    practical: int = Field(..., ge=0, le=100)
    investigative: int = Field(..., ge=0, le=100)

    top_strength: str
    learning_style: Literal["Visual", "Auditory", "Kinesthetic", "Reading"]

    potential_career_paths: List[CareerPath]  # exactly 3
    recommended_next_steps: List[str]         # >= 2
    confidence_indicators: ConfidenceIndicators
    interest_distribution: InterestDistribution

    welcome_statement: str
    your_natural_inclination: str
    possible_roadblocks: List[str]            
    remarks: str

    profile_in_a_gist: ProfileInAGist
    final_note: str

    