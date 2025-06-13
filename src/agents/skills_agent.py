import json
from typing import List, Dict
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent


class SkillsAgent(BaseAgent):
    def __init__(self, openai_api_key: str):
        super().__init__(openai_api_key)

        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=300
        )

        self.skills_database = self._build_skills_database()

    def _build_skills_database(self) -> Dict:
        return {
            "AI ENGINEER": {
                "core_skills": [
                    "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
                    "Scikit-learn", "Pandas", "NumPy", "Computer Vision", "Natural Language Processing"
                ],
                "advanced_skills": [
                    "MLOps", "Kubernetes", "Docker", "AWS", "Azure", "GCP", "Apache Airflow"
                ]
            },
            "DATA SCIENCE ENGINEER": {
                "core_skills": [
                    "Python", "R", "SQL", "Statistics", "Data Analysis", "Pandas", "NumPy"
                ],
                "ml_skills": [
                    "Machine Learning", "Scikit-learn", "XGBoost", "Apache Spark"
                ]
            },
            "PYTHON DEVELOPER": {
                "core_skills": [
                    "Python", "Django", "Flask", "FastAPI", "REST API", "PostgreSQL"
                ],
                "web_skills": [
                    "HTML", "CSS", "JavaScript", "React", "Docker"
                ]
            }
        }

    def infer_skills_from_job(self, job: Dict, job_category: str) -> List[str]:
        inferred_skills = []
        title_lower = job['title'].lower()

        category_skills = self.skills_database.get(job_category, {})
        core_skills = category_skills.get('core_skills', [])
        inferred_skills.extend(core_skills[:5])

        title_keywords = {
            'senior': category_skills.get('advanced_skills', [])[:3],
            'machine learning': ['Machine Learning', 'Python', 'Scikit-learn'],
            'data scientist': ['Python', 'R', 'SQL', 'Statistics'],
            'python': ['Python', 'Django', 'Flask'],
            'ai': ['AI', 'Machine Learning', 'Python']
        }

        for keyword, skills in title_keywords.items():
            if keyword in title_lower:
                inferred_skills.extend(skills)

        return list(set(inferred_skills))

    def enhance_with_ai(self, job: Dict, base_skills: List[str]) -> List[str]:
        try:
            prompt = f"""
            Based on this job, suggest 3 additional technical skills:

            Title: {job['title']}
            Company: {job['company']}
            Location: {job['location']}
            Current skills: {', '.join(base_skills[:5])}

            Return only JSON array: ["skill1", "skill2", "skill3"]
            """

            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()

            if content.startswith('```'):
                content = content.split('\n', 1)[1].split('\n```')[0]

            additional_skills = json.loads(content)

            if isinstance(additional_skills, list):
                return [skill.strip() for skill in additional_skills if isinstance(skill, str)]

        except Exception as e:
            print(f"AI enhancement failed: {e}")

        return []