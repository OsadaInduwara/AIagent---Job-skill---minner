import os
from abc import ABC, abstractmethod
from typing import List, Dict


class BaseAgent(ABC):
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key

    @abstractmethod
    def infer_skills_from_job(self, job: Dict, job_category: str) -> List[str]:
        pass

    @abstractmethod
    def enhance_with_ai(self, job: Dict, base_skills: List[str]) -> List[str]:
        pass