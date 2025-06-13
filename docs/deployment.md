# Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- Chrome browser (for Selenium)
- OpenAI API key

### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/ai-job-skills-analyzer.git
cd ai-job-skills-analyzer
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env file with your OpenAI API key
```

5. **Create Data Directory**
```bash
mkdir -p data logs
```

### Running the Application

**Basic Usage**:
```python
from src.workflows.skills_workflow import SkillsExtractionWorkflow

workflow = SkillsExtractionWorkflow(openai_api_key="your_key")
results = workflow.run_analysis(
    job_category="AI ENGINEER",
    location="Sri Lanka",
    date_filter="Last Week",
    search_keywords=["AI Engineer", "Machine Learning Engineer"]
)
```

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

# Install Chrome for Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "src.main"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  job-analyzer:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-3.5-turbo
      - MAX_JOBS_PER_SEARCH=10
      - SCRAPING_DELAY=2
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

**Run with Docker Compose**:
```bash
docker-compose up -d
```

## Cloud Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security group allowing HTTP/HTTPS

2. **Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

3. **Deploy Application**
```bash
git clone https://github.com/yourusername/ai-job-skills-analyzer.git
cd ai-job-skills-analyzer
cp .env.example .env
# Edit .env with your API keys
docker-compose up -d
```

### Environment Variables

**Production Environment**:
```bash
# .env for production
OPENAI_API_KEY=your_production_key
OPENAI_MODEL=gpt-3.5-turbo
MAX_JOBS_PER_SEARCH=20
SCRAPING_DELAY=3
DATA_DIR=/app/data
LOG_LEVEL=INFO
```

## Monitoring & Logging

### Application Logs
```python
# Logs are stored in logs/ directory
# Format: app_YYYYMMDD.log
```

### Health Checks
```bash
# Check if application is running
docker ps
docker logs job-analyzer_job-analyzer_1
```

### Performance Monitoring
- Monitor CPU usage during scraping operations
- Track memory usage for large datasets
- Monitor OpenAI API rate limits

## Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly

### Web Scraping Ethics
- Respect robots.txt files
- Implement appropriate delays
- Don't overload target servers

### Data Security
- Encrypt sensitive data at rest
- Use HTTPS for all external communications
- Regular security updates

## Troubleshooting

### Common Issues

**Chrome Driver Issues**:
```bash
# Update webdriver
pip install --upgrade webdriver-manager
```

**Memory Issues**:
```bash
# Reduce batch size
export MAX_JOBS_PER_SEARCH=5
```

**Rate Limiting**:
```bash
# Increase delays
export SCRAPING_DELAY=5
```

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Scaling Considerations

### Horizontal Scaling
- Run multiple instances with different job categories
- Use load balancer for API endpoints
- Implement job queue for batch processing

### Database Integration
- Consider PostgreSQL for production data storage
- Implement data archiving strategies
- Add database connection pooling

### Performance Optimization
- Cache frequently accessed data
- Implement async processing
- Use CDN for static assets