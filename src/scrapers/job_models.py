from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    search_keyword: str
    scraped_at: str
    source: str = "LinkedIn"
    url: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "search_keyword": self.search_keyword,
            "scraped_at": self.scraped_at,
            "source": self.source,
            "url": self.url,
            "description": self.description
        }


@dataclass
class JobWithSkills:
    job: JobPosting
    skills: List[str]
    skills_source: str = "unknown"
    skills_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            **self.job.to_dict(),
            "skills": self.skills,
            "skills_source": self.skills_source,
            "skills_count": len(self.skills)
        }