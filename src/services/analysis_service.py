from typing import Dict, List, Any
from collections import Counter


class AnalysisService:
    def __init__(self):
        pass

    def analyze_skills_frequency(self, jobs_with_skills: List[Dict]) -> List[Dict]:
        skill_freq = {}
        total_jobs = len(jobs_with_skills)

        for job in jobs_with_skills:
            if job.get("skills"):
                for skill in job["skills"]:
                    skill_freq[skill] = skill_freq.get(skill, 0) + 1

        skill_frequencies = []
        for skill, count in sorted(skill_freq.items(), key=lambda x: x[1], reverse=True):
            skill_frequencies.append({
                "skill": skill,
                "frequency": count,
                "percentage": round((count / total_jobs) * 100, 1) if total_jobs > 0 else 0
            })

        return skill_frequencies

    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        categories = {
            "Programming Languages": ["Python", "Java", "JavaScript", "R", "Scala", "Go", "C++"],
            "ML/AI Frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost"],
            "Cloud Platforms": ["AWS", "Azure", "GCP", "Google Cloud"],
            "Databases": ["SQL", "PostgreSQL", "MongoDB", "Redis", "MySQL"],
            "Tools & Platforms": ["Docker", "Kubernetes", "Git", "Jenkins", "Airflow"]
        }

        categorized_skills = {category: [] for category in categories}
        uncategorized = []

        for skill in skills:
            categorized = False
            for category, keywords in categories.items():
                if any(keyword.lower() in skill.lower() for keyword in keywords):
                    categorized_skills[category].append(skill)
                    categorized = True
                    break

            if not categorized:
                uncategorized.append(skill)

        if uncategorized:
            categorized_skills["Other"] = uncategorized

        return {k: v for k, v in categorized_skills.items() if v}

    def find_skill_combinations(self, jobs_with_skills: List[Dict], min_frequency: int = 2) -> List[Dict]:
        skill_pairs = {}

        for job in jobs_with_skills:
            skills = job.get("skills", [])
            if len(skills) > 1:
                for i, skill1 in enumerate(skills):
                    for skill2 in skills[i + 1:]:
                        pair = tuple(sorted([skill1, skill2]))
                        skill_pairs[pair] = skill_pairs.get(pair, 0) + 1

        combinations = []
        for (skill1, skill2), count in skill_pairs.items():
            if count >= min_frequency:
                combinations.append({
                    "skills": [skill1, skill2],
                    "frequency": count,
                    "percentage": round((count / len(jobs_with_skills)) * 100, 1)
                })

        return sorted(combinations, key=lambda x: x["frequency"], reverse=True)

    def get_company_analysis(self, jobs_with_skills: List[Dict]) -> Dict[str, Any]:
        companies = [job.get("company", "") for job in jobs_with_skills if job.get("company")]
        company_counts = Counter(companies)

        return {
            "total_companies": len(company_counts),
            "top_companies": dict(company_counts.most_common(10)),
            "unique_companies": len(set(companies))
        }

    def get_location_analysis(self, jobs_with_skills: List[Dict]) -> Dict[str, Any]:
        locations = [job.get("location", "") for job in jobs_with_skills if job.get("location")]
        location_counts = Counter(locations)

        return {
            "total_locations": len(location_counts),
            "top_locations": dict(location_counts.most_common(10)),
            "geographic_distribution": dict(location_counts)
        }