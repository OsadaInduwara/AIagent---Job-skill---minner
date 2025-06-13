# AI Job Skills Analyzer

An AI-powered system that scrapes job postings and extracts in-demand skills using multi-agent workflows with LangGraph.

## Features

- **Multi-Agent Architecture**: Specialized agents for scraping, analysis, and data processing
- **LangGraph Workflows**: Orchestrated task execution with state management
- **AI-Enhanced Skills Extraction**: Combines rule-based inference with LLM enhancement
- **Location-Based Filtering**: Precise geographic job targeting
- **Real-time Analysis**: Job market insights and skill demand trends

## Quick Start

### Installation
```bash
git clone https://github.com/osadainduwara/ai-job-skills-analyzer.git
cd ai-job-skills-analyzer
pip install -r requirements.txt
```

### Setup
```bash
cp .env.example .env
```

### Basic Usage
```python
from src.workflows.skills_workflow import SkillsExtractionWorkflow
from src.config.job_keywords import JobKeywords

# Initialize workflow
workflow = SkillsExtractionWorkflow(openai_api_key="your_key")

# Run analysis
results = workflow.run_analysis(
    job_category="AI ENGINEER",
    location="Sri Lanka", 
    date_filter="Last Week",
    search_keywords=JobKeywords.get_search_keywords("AI ENGINEER")
)

print(f"Found {len(results['jobs_with_skills'])} jobs")
print(f"Extracted {len(results['extracted_skills'])} skills")
```

## Architecture

```
Job Scraper → Skills Agent → Analysis Engine → Data Storage
     ↓             ↓              ↓              ↓
LinkedIn API → LLM Enhancement → Statistics → JSON/CSV Export
```

## Supported Job Categories

- **AI ENGINEER**: ML, NLP, Computer Vision roles
- **DATA SCIENCE ENGINEER**: Analytics and data engineering  
- **PYTHON DEVELOPER**: Backend and full-stack development

## Technical Stack

- **LangGraph**: Multi-agent workflow orchestration
- **OpenAI GPT**: Skills extraction and enhancement
- **Selenium**: Web scraping automation
- **Python**: Core backend processing

## Project Structure

```
src/
├── agents/          # AI agents (base, skills)
├── workflows/       # LangGraph workflows
├── scrapers/        # Web scraping logic
├── services/        # Analysis and storage
├── config/          # Settings and keywords
└── utils/           # Logging utilities
```

## Sample Output

```json
{
  "job_category": "AI ENGINEER",
  "location": "Sri Lanka",
  "total_jobs": 12,
  "top_skills": [
    {"skill": "Python", "frequency": 10, "percentage": 83.3},
    {"skill": "Machine Learning", "frequency": 8, "percentage": 66.7},
    {"skill": "TensorFlow", "frequency": 6, "percentage": 50.0}
  ]
}
```

## Documentation

- [Deployment Guide](docs/deployment.md)

## Requirements

- Python 3.12+
- OpenAI API key
- Chrome browser (for Selenium)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

⭐ Star this repo if you find it useful!