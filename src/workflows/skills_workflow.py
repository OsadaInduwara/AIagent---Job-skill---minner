import json
import time
import random
from typing import Dict, List
from datetime import datetime
import os

from langgraph.graph import StateGraph, END

from .workflow_state import JobSkillsState
from ..agents.skills_agent import SkillsAgent
from ..scrapers.linkedin_scraper import LinkedInScraper
from ..services.analysis_service import AnalysisService
from ..services.storage_service import StorageService


class SkillsExtractionWorkflow:
    def __init__(self, openai_api_key: str):
        os.environ["OPENAI_API_KEY"] = openai_api_key

        self.scraper = LinkedInScraper()
        self.skills_agent = SkillsAgent(openai_api_key)
        self.analysis_service = AnalysisService()
        self.storage_service = StorageService()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = StateGraph(JobSkillsState)

        workflow.add_node("search", self.search_jobs_node)
        workflow.add_node("filter_location", self.filter_location_node)
        workflow.add_node("infer", self.infer_skills_node)
        workflow.add_node("save", self.save_results_node)

        workflow.add_edge("search", "filter_location")
        workflow.add_edge("filter_location", "infer")
        workflow.add_edge("infer", "save")
        workflow.add_edge("save", END)

        workflow.set_entry_point("search")

        return workflow.compile()

    def search_jobs_node(self, state: JobSkillsState) -> JobSkillsState:
        state["current_step"] = f"Searching for {state['job_category']} jobs in {state['location']}..."

        try:
            all_jobs = []
            search_keywords = state["search_keywords"]

            for i, keyword in enumerate(search_keywords[:3]):
                state["current_step"] = f"Searching '{keyword}' in {state['location']} ({i + 1}/3)..."

                jobs = self.scraper.search_jobs_for_keyword(
                    keyword,
                    state["location"],
                    state["date_filter"]
                )
                all_jobs.extend(jobs)

                time.sleep(random.uniform(3, 5))

            unique_jobs = self._remove_duplicate_jobs(all_jobs)
            state["raw_jobs"] = unique_jobs
            state["current_step"] = f"Found {len(unique_jobs)} jobs (before location filtering)"

        except Exception as e:
            print(f"Search error: {e}")
            state["error_messages"].append(f"Search error: {str(e)}")

        return state

    def filter_location_node(self, state: JobSkillsState) -> JobSkillsState:
        state["current_step"] = f"Filtering jobs to ONLY {state['location']}..."

        user_location = state["location"].lower().strip()
        location_filtered_jobs = []

        print(f"\n🔍 STRICT LOCATION FILTER: Only keeping jobs from '{user_location}'")

        for job in state["raw_jobs"]:
            job_location = job.get("location", "").lower().strip()

            if self._is_location_match(job_location, user_location):
                location_filtered_jobs.append(job)
                print(f" KEEP: {job['title']} at {job['company']} - Location: {job['location']}")
            else:
                print(
                    f" REJECT: {job['title']} at {job['company']} - Location: {job['location']} (not {state['location']})")

        state["filtered_jobs"] = location_filtered_jobs

        rejected_count = len(state["raw_jobs"]) - len(location_filtered_jobs)
        state[
            "current_step"] = f"Kept {len(location_filtered_jobs)} jobs from {state['location']}, rejected {rejected_count} from other locations"

        print(f"\n LOCATION FILTER RESULTS:")
        print(f"Total scraped: {len(state['raw_jobs'])}")
        print(f"Kept ({user_location}): {len(location_filtered_jobs)}")
        print(f"Rejected (other locations): {rejected_count}")

        return state

    def infer_skills_node(self, state: JobSkillsState) -> JobSkillsState:
        state["current_step"] = "Inferring skills from location-filtered jobs..."

        jobs_with_skills = []
        all_skills = set()

        for job in state["filtered_jobs"]:
            try:
                inferred_skills = self.skills_agent.infer_skills_from_job(job, state["job_category"])
                ai_skills = self.skills_agent.enhance_with_ai(job, inferred_skills)

                final_skills = list(set(inferred_skills + ai_skills))

                jobs_with_skills.append({
                    **job,
                    "skills": final_skills,
                    "skills_source": "inferred + ai_enhanced",
                    "skills_count": len(final_skills)
                })

                all_skills.update(final_skills)

            except Exception as e:
                print(f"Error inferring skills for {job['title']}: {e}")
                jobs_with_skills.append({
                    **job,
                    "skills": [],
                    "skills_source": "error",
                    "skills_count": 0
                })

        state["jobs_with_skills"] = jobs_with_skills
        state["extracted_skills"] = sorted(list(all_skills))
        state[
            "current_step"] = f"Extracted {len(all_skills)} skills from {len(jobs_with_skills)} {state['location']} jobs"

        return state

    def save_results_node(self, state: JobSkillsState) -> JobSkillsState:
        state["current_step"] = "Saving results..."

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"location_filtered_analysis_{timestamp}.json"

            save_data = {
                "job_category": state["job_category"],
                "location": state["location"],
                "date_filter": state["date_filter"],
                "jobs_with_skills": state["jobs_with_skills"],
                "extracted_skills": state["extracted_skills"],
                "location_filter_stats": {
                    "total_scraped": len(state["raw_jobs"]),
                    "location_filtered": len(state["filtered_jobs"]),
                    "rejected_count": len(state["raw_jobs"]) - len(state["filtered_jobs"]),
                    "filter_success_rate": f"{(len(state['filtered_jobs']) / max(len(state['raw_jobs']), 1) * 100):.1f}%"
                },
                "summary": {
                    "total_jobs": len(state["jobs_with_skills"]),
                    "total_skills": len(state["extracted_skills"]),
                    "analysis_timestamp": timestamp,
                    "method": "strict_location_filtering"
                }
            }

            self.storage_service.save_results(filename, save_data)
            state[
                "current_step"] = f"Results saved - {len(state['jobs_with_skills'])} {state['location']} jobs analyzed"

        except Exception as e:
            state["error_messages"].append(f"Save error: {str(e)}")

        return state

    def _remove_duplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        seen = set()
        unique_jobs = []

        for job in jobs:
            identifier = f"{job['title'].lower()}_{job['company'].lower()}"
            if identifier not in seen:
                seen.add(identifier)
                unique_jobs.append(job)

        return unique_jobs

    def _is_location_match(self, job_location: str, user_location: str) -> bool:
        if not job_location or not user_location:
            return False

        if user_location in job_location or job_location in user_location:
            return True

        location_mappings = {
            "sri lanka": ["sri lanka", "srilanka", "lk", "colombo", "kandy", "galle", "jaffna"],
            "usa": ["united states", "usa", "us", "america"],
            "uk": ["united kingdom", "uk", "england", "britain"],
            "india": ["india", "bharat"],
            "singapore": ["singapore", "sg"],
            "canada": ["canada", "ca"],
            "australia": ["australia", "au"],
            "remote": ["remote", "work from home", "wfh", "anywhere", "distributed"]
        }

        for main_location, variations in location_mappings.items():
            if user_location in variations:
                return any(variation in job_location for variation in variations)

        city_mappings = {
            "colombo": ["colombo", "sri lanka"],
            "kandy": ["kandy", "sri lanka"],
            "new york": ["new york", "ny", "usa", "united states"],
            "san francisco": ["san francisco", "sf", "california", "usa"],
            "london": ["london", "uk", "england", "united kingdom"],
            "mumbai": ["mumbai", "india"],
            "bangalore": ["bangalore", "bengaluru", "india"],
            "toronto": ["toronto", "canada"],
            "sydney": ["sydney", "australia"]
        }

        for city, variations in city_mappings.items():
            if user_location == city:
                return any(variation in job_location for variation in variations)

        return False

    def run_analysis(self, job_category: str, location: str, date_filter: str, search_keywords: List[str]) -> Dict:
        initial_state = JobSkillsState(
            job_category=job_category,
            location=location,
            date_filter=date_filter,
            search_keywords=search_keywords,
            raw_jobs=[],
            filtered_jobs=[],
            extracted_skills=[],
            jobs_with_skills=[],
            error_messages=[],
            current_step="Starting..."
        )

        final_state = self.workflow.invoke(initial_state)
        return final_state