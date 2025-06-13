class JobKeywords:
    JOB_CATEGORIES = {
        "AI ENGINEER": {
            "keywords": [
                "AI Engineer", "Artificial Intelligence Engineer", "Machine Learning Engineer",
                "ML Engineer", "AI Developer", "AI Specialist", "AI Researcher",
                "NLP Engineer", "Computer Vision Engineer", "Deep Learning Engineer",
                "Neural Network Engineer", "LLM Engineer", "Generative AI Engineer",
                "MLOps Engineer", "LLMOps Engineer", "AI Platform Engineer",
                "ML Infrastructure Engineer", "AI Systems Engineer",
                "Applied AI Scientist", "AI Research Engineer", "Machine Learning Scientist",
                "AI Solutions Engineer", "Conversational AI Engineer",
                "Prompt Engineer", "RAG Engineer", "Foundation Model Engineer",
                "AI Product Manager", "AI Architect"
            ],
            "description": "AI Engineering roles including ML, NLP, Computer Vision, and AI Operations"
        },

        "DATA SCIENCE ENGINEER": {
            "keywords": [
                "Data Scientist", "Senior Data Scientist", "Principal Data Scientist",
                "Data Science Engineer", "Applied Data Scientist", "Research Data Scientist",
                "Data Analyst", "Senior Data Analyst", "Business Intelligence Analyst",
                "Analytics Engineer", "Quantitative Analyst", "Statistical Analyst",
                "Data Engineer", "Big Data Engineer", "Data Platform Engineer",
                "Data Infrastructure Engineer", "ETL Developer", "Data Architect",
                "Biostatistician", "Econometrician", "Operations Research Analyst",
                "Data Mining Engineer", "Predictive Analytics Engineer",
                "BI Developer", "BI Analyst", "Business Data Analyst",
                "Reporting Analyst", "Insights Analyst"
            ],
            "description": "Data Science and Analytics roles including engineering and analysis"
        },

        "PYTHON DEVELOPER": {
            "keywords": [
                "Python Developer", "Senior Python Developer", "Python Engineer",
                "Python Software Engineer", "Full Stack Python Developer",
                "Django Developer", "Flask Developer", "FastAPI Developer",
                "Python Web Developer", "Backend Python Developer",
                "Python/React Developer", "Python/JavaScript Developer",
                "Python Full Stack Engineer", "Python API Developer",
                "Python Automation Engineer", "Python DevOps Engineer",
                "Python Cloud Engineer", "Python Microservices Developer",
                "Python Fintech Developer", "Python Game Developer",
                "Python Desktop Application Developer", "Python Mobile Backend Developer"
            ],
            "description": "Python development roles across web, backend, and specialized applications"
        }
    }

    DATE_FILTERS = {
        "Today": "r86400",
        "Last Week": "r604800",
        "Last 2 Weeks": "r1209600",
        "Last 3 Weeks": "r1814400",
        "Last Month": "r2592000"
    }

    @staticmethod
    def get_search_keywords(job_category: str) -> list:
        return JobKeywords.JOB_CATEGORIES.get(job_category, {}).get("keywords", [])

    @staticmethod
    def get_date_filter(date_range: str) -> str:
        return JobKeywords.DATE_FILTERS.get(date_range, "r604800")