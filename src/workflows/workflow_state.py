from typing import Dict, List, TypedDict
from datetime import datetime


class JobSkillsState(TypedDict):
    job_category: str
    location: str
    date_filter: str
    search_keywords: List[str]
    raw_jobs: List[Dict]
    filtered_jobs: List[Dict]
    extracted_skills: List[str]
    jobs_with_skills: List[Dict]
    error_messages: List[str]
    current_step: str