# Pseudo-code for the logic implementation
from models.user_profile import UserProfile
from models.job_requirement import JobRequirement
from models.alignment import AlignmentAnalysis

def generate_alignment(user: UserProfile, job: JobRequirement) -> AlignmentAnalysis:
    """
    This function PROVES the dependency.
    It cannot run without 'user' and 'job' inputs.
    """
    
    # 1. Extract the "Top 6 Attributes" from the job_requirement
    target_attributes = job.top_attributes 
    
    # 2. Loop through attributes and search the user.experience for evidence
    # (This is where your LLM or Logic goes)
    # prompt = f"Does {user.raw_text} have experience in {target_attributes}?"
    
    # 3. Construct the AlignmentAnalysis object
    return AlignmentAnalysis(
        job_id=job.job_id,
        user_profile_id=user.profile_id,
        alignment_rows=[...], # populated from LLM analysis
        scores=[...],         # populated from LLM analysis
        overall_match_percentage=85
    )