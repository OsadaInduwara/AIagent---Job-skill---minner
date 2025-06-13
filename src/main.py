import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, List
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

try:
    from workflows.skills_workflow import SkillsExtractionWorkflow
    from config.job_keywords import JobKeywords
    from config.settings import Config
    from services.analysis_service import AnalysisService
except ImportError:
    from src.workflows.skills_workflow import SkillsExtractionWorkflow
    from src.config.job_keywords import JobKeywords
    from src.config.settings import Config
    from src.services.analysis_service import AnalysisService

st.set_page_config(
    page_title="Skills Miner",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: #0a0a0a;
    }
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .sub-header {
        font-size: 1.3rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    .control-panel {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #FF6B6B;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.2);
    }
    .control-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .control-section h3 {
        color: #ffffff;
    }
    .search-button {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 3rem;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(78, 205, 196, 0.4);
        transition: all 0.3s ease;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 2px solid;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    }
    .metric-card:nth-child(1) { border-color: #FF6B6B; }
    .metric-card:nth-child(2) { border-color: #FF8E53; }
    .metric-card:nth-child(3) { border-color: #FFE66D; }
    .metric-card:nth-child(4) { border-color: #4ECDC4; }
    .metric-card h3 {
        color: #ffffff;
    }
    .metric-card p {
        color: #b0b0b0;
    }
    .skill-pill {
        display: inline-block;
        background: linear-gradient(135deg, #FF8E53 0%, #FFE66D 100%);
        color: #000000;
        padding: 0.6rem 1.5rem;
        margin: 0.4rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 10px rgba(255, 142, 83, 0.3);
        transition: all 0.3s ease;
    }
    .skill-pill:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(255, 142, 83, 0.4);
    }
    .featured-card {
        background: linear-gradient(135deg, #16213e 0%, #0f172a 100%);
        border: 2px solid #4ECDC4;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 15px 35px rgba(78, 205, 196, 0.2);
    }
    .job-card {
        background: #1a1a2e;
        border-left: 5px solid #FF6B6B;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
        color: #ffffff;
    }
    .job-card:hover {
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        transform: translateX(5px);
    }
    .welcome-card {
        background: linear-gradient(135deg, #16213e 0%, #0f172a 100%);
        border: 2px solid #FF8E53;
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.2);
        color: white;
    }
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1rem 0;
    }
    .tab-section {
        background: #1a1a2e;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-top: 2rem;
        border: 1px solid #2a2a3e;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #16213e;
        border-radius: 15px;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: white;
        font-weight: 600;
        border-radius: 10px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
    }
    .category-badge {
        background: linear-gradient(135deg, #FFE66D 0%, #FF8E53 100%);
        color: #000000;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
    }
    .info-box {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: #000000;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-weight: 600;
    }
    .stSelectbox label {
        color: #ffffff !important;
    }
    .stTextInput label {
        color: #ffffff !important;
    }
    .stExpander {
        background: #1a1a2e;
        border: 1px solid #2a2a3e;
    }
    .stExpander p {
        color: #ffffff;
    }
    [data-testid="stExpander"] div[role="button"] p {
        color: #ffffff;
    }
    .stCheckbox label {
        color: #ffffff !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #ffffff;
    }
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">Skills Miner</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Extract skills from AI, Machine Learning, and Data Science job postings using '
        'LangGraph & LangChain</p>',
        unsafe_allow_html=True)

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    if st.session_state.analysis_results:
        render_results()
    else:
        render_main_interface()


def render_main_interface():
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: white; text-align: center; margin-bottom: 2rem;">🚀 Start Your Search</h2>',
                    unsafe_allow_html=True)

        st.markdown('<div class="control-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FF6B6B; margin-bottom: 1rem;">📋 Job Category</h3>', unsafe_allow_html=True)
        job_categories = list(JobKeywords.JOB_CATEGORIES.keys())
        selected_category = st.selectbox(
            "",
            job_categories,
            help="Choose the type of AI/ML jobs to analyze",
            label_visibility="collapsed"
        )

        category_info = JobKeywords.JOB_CATEGORIES[selected_category]
        st.markdown(f'<div class="info-box">{category_info["description"]}</div>', unsafe_allow_html=True)

        with st.expander("🔍 Search Keywords Preview"):
            keywords = category_info['keywords'][:8]
            keywords_html = ""
            for keyword in keywords:
                keywords_html += f'<span class="category-badge">{keyword}</span>'
            if len(category_info['keywords']) > 8:
                keywords_html += f'<span class="category-badge">+{len(category_info["keywords"]) - 8} more</span>'
            st.markdown(keywords_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="control-section">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #FF8E53; margin-bottom: 1rem;">📅 Date Filter</h3>', unsafe_allow_html=True)
            date_options = list(JobKeywords.DATE_FILTERS.keys())
            selected_date = st.selectbox(
                "",
                date_options,
                index=1,
                help="Filter jobs by when they were posted",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="control-section">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #4ECDC4; margin-bottom: 1rem;">📍 Location</h3>', unsafe_allow_html=True)
            location = st.text_input(
                "",
                value="United States",
                help="Enter location for job search",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
                run_analysis(selected_category, location, selected_date)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="welcome-card">
        <h3 style="color: white; text-align: center; margin-bottom: 2rem;">✨ How This Works</h3>

        <h4 style="color: #FFE66D; margin-bottom: 1rem;">🔄 LangGraph Workflow Pipeline:</h4>
        <p style="color: #ffffff; margin-bottom: 0.5rem;">1. <strong style="color: #FF6B6B;">Job Search Node</strong> - Multi-keyword LinkedIn scraping</p>
        <p style="color: #ffffff; margin-bottom: 0.5rem;">2. <strong style="color: #FF8E53;">Location Filter Node</strong> - Strict geographic filtering</p>
        <p style="color: #ffffff; margin-bottom: 0.5rem;">3. <strong style="color: #FFE66D;">Skills Extraction Node</strong> - AI-powered skill identification</p>
        <p style="color: #ffffff; margin-bottom: 1.5rem;">4. <strong style="color: #4ECDC4;">Save Results Node</strong> - Structured data persistence</p>

        <h4 style="color: #FFE66D; margin-bottom: 1rem;">🤖 LangChain AI Agents:</h4>
        <p style="color: #ffffff; margin-bottom: 0.5rem;">• <strong>Skills Agent</strong> - GPT-powered skill extraction</p>
        <p style="color: #ffffff;">• <strong>Enhancement Agent</strong> - Contextual skill augmentation</p>
        </div>
        """, unsafe_allow_html=True)


def run_analysis(job_category: str, location: str, date_filter: str):
    try:
        search_keywords = JobKeywords.get_search_keywords(job_category)

        if not search_keywords:
            st.error(f"No keywords found for job category: {job_category}")
            return

        with st.spinner("🚀 Initializing LangGraph Workflow..."):
            workflow = SkillsExtractionWorkflow(openai_api_key=Config.OPENAI_API_KEY)

        with st.spinner(f"🔍 Searching for {job_category} jobs..."):
            progress_bar = st.progress(0)

            progress_bar.progress(33)
            st.write("📊 Scraping LinkedIn...")

            results = workflow.run_analysis(
                job_category=job_category,
                location=location,
                date_filter=date_filter,
                search_keywords=search_keywords
            )

            progress_bar.progress(66)
            st.write("🤖 LangChain agent extracting skills...")

            st.session_state.analysis_results = results

            progress_bar.progress(100)
            st.success("✅ LangGraph workflow completed!")

            st.rerun()

    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        st.error("Make sure your OpenAI API key is valid and has credits")


def render_results():
    results = st.session_state.analysis_results

    if results.get("error_messages"):
        for error in results["error_messages"]:
            st.error(f"❌ {error}")
        return

    jobs = results.get("jobs_with_skills", [])
    skills = results.get("extracted_skills", [])

    st.markdown(f'<h1 class="section-title">📊 {results.get("job_category", "Job")} Skills Analysis</h1>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    jobs_with_skills = len([j for j in jobs if j.get("skills")])
    unique_companies = len(set([job.get("company", "") for job in jobs if job.get("company")]))

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #FF6B6B; margin: 0; font-size: 2.5rem;">{len(jobs)}</h3>
            <p style="color: #ffffff; margin: 0.5rem 0 0 0; font-weight: 600;">Total Jobs Found</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #FF8E53; margin: 0; font-size: 2.5rem;">{jobs_with_skills}</h3>
            <p style="color: #ffffff; margin: 0.5rem 0 0 0; font-weight: 600;">Jobs with Skills</p>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #FFE66D; margin: 0; font-size: 2.5rem;">{len(skills)}</h3>
            <p style="color: #ffffff; margin: 0.5rem 0 0 0; font-weight: 600;">Unique Skills</p>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <h3 style="color: #4ECDC4; margin: 0; font-size: 2.5rem;">{unique_companies}</h3>
            <p style="color: #ffffff; margin: 0.5rem 0 0 0; font-weight: 600;">Companies</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown(
        f'<div class="info-box">📍 Location: {results.get("location")} | 📅 Filter: {results.get("date_filter")}</div>',
        unsafe_allow_html=True)

    st.markdown('<div class="tab-section">', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🎯 Skills Overview", "💼 Job Details", "📈 Skills Analytics"])

    with tab1:
        render_skills_overview(skills, jobs)

    with tab2:
        render_job_details(jobs)

    with tab3:
        render_skills_analytics(jobs, skills)

    st.markdown('</div>', unsafe_allow_html=True)


def render_skills_overview(skills: List[str], jobs: List[Dict]):
    if not skills:
        st.warning("⚠️ No skills extracted. Try a different search or check if jobs have descriptions.")
        return

    st.markdown("""
    <div class="featured-card">
        <h3 style="color: white; margin-bottom: 1.5rem; text-align: center;">🎯 Extracted Technical Skills</h3>
    """, unsafe_allow_html=True)

    if skills:
        skills_html = '<div style="text-align: center;">'
        for skill in skills:
            skills_html += f'<span class="skill-pill">{skill}</span>'
        skills_html += '</div>'
        st.markdown(skills_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="featured-card" style="border-color: #FF6B6B;">
            <h4 style="color: white; margin-bottom: 1rem;">📊 Quick Stats</h4>
        """, unsafe_allow_html=True)

        analysis_service = AnalysisService()
        skill_frequencies = analysis_service.analyze_skills_frequency(jobs)

        if skill_frequencies:
            most_common = skill_frequencies[0]
            st.markdown(
                f'<p style="color: #ffffff;"><strong style="color: #FF6B6B;">🏆 Most Common Skill:</strong> {most_common["skill"]} ({most_common["frequency"]} jobs)</p>',
                unsafe_allow_html=True)

            avg_skills_per_job = sum(len(job.get("skills", [])) for job in jobs if job.get("skills")) / max(
                len([j for j in jobs if j.get("skills")]), 1)
            st.markdown(
                f'<p style="color: #ffffff;"><strong style="color: #FF8E53;">📈 Avg Skills per Job:</strong> {avg_skills_per_job:.1f}</p>',
                unsafe_allow_html=True)

            jobs_with_skills_pct = (len([j for j in jobs if j.get("skills")]) / max(len(jobs), 1)) * 100
            st.markdown(
                f'<p style="color: #ffffff;"><strong style="color: #4ECDC4;">✅ Success Rate:</strong> {jobs_with_skills_pct:.1f}% jobs analyzed</p>',
                unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="featured-card" style="border-color: #FFE66D;">
            <h4 style="color: white; margin-bottom: 1rem;">📂 Skill Categories</h4>
        """, unsafe_allow_html=True)

        analysis_service = AnalysisService()
        categories = analysis_service.categorize_skills(skills)

        for category, category_skills in categories.items():
            st.markdown(
                f'<p style="color: #ffffff;"><strong style="color: #FFE66D;">{category}:</strong> {len(category_skills)} skills</p>',
                unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def render_job_details(jobs: List[Dict]):
    if not jobs:
        st.warning("⚠️ No jobs found")
        return

    st.markdown('<h3 class="section-title">💼 Job Listings</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        show_only_with_skills = st.checkbox("Show only jobs with extracted skills", value=True)

    with col2:
        if jobs:
            companies = sorted(list(set([job.get("company", "Unknown") for job in jobs])))
            selected_company = st.selectbox("Filter by Company", ["All"] + companies)

    filtered_jobs = jobs

    if show_only_with_skills:
        filtered_jobs = [job for job in filtered_jobs if job.get("skills")]

    if selected_company != "All":
        filtered_jobs = [job for job in filtered_jobs if job.get("company") == selected_company]

    st.markdown(f'<p style="color: #ffffff;">📊 Showing {len(filtered_jobs)} of {len(jobs)} jobs</p>',
                unsafe_allow_html=True)

    for i, job in enumerate(filtered_jobs):
        with st.expander(f"🏢 {job.get('title', 'Unknown Title')} at {job.get('company', 'Unknown Company')}"):
            st.markdown(f'''
            <div class="job-card">
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
                    <div>
                        <p style="color: #ffffff;"><strong style="color: #FF6B6B;">🏢 Company:</strong> {job.get('company', 'Not specified')}</p>
                        <p style="color: #ffffff;"><strong style="color: #FF8E53;">📍 Location:</strong> {job.get('location', 'Not specified')}</p>
                        <p style="color: #ffffff;"><strong style="color: #FFE66D;">🔍 Found via:</strong> {job.get('search_keyword', 'Direct search')}</p>
                        <p style="color: #ffffff;"><strong style="color: #4ECDC4;">📅 Scraped:</strong> {job.get('scraped_at', 'Unknown')[:19]}</p>
                    </div>
                    <div>
            ''', unsafe_allow_html=True)

            skills = job.get("skills")
            if skills:
                st.markdown(
                    f'<p style="color: #ffffff;"><strong style="color: #FF6B6B;">🎯 Skills Found ({len(skills)}):</strong></p>',
                    unsafe_allow_html=True)
                skills_list = ""
                for skill in skills:
                    skills_list += f'<span class="skill-pill" style="font-size: 0.85rem; padding: 0.4rem 1rem;">{skill}</span>'
                st.markdown(skills_list, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #ffffff;"><strong>🎯 Skills:</strong> None extracted</p>',
                            unsafe_allow_html=True)

            st.markdown('</div></div></div>', unsafe_allow_html=True)


def render_skills_analytics(jobs: List[Dict], skills: List[str]):
    if not skills:
        st.warning("⚠️ No skills data available for analytics")
        return

    analysis_service = AnalysisService()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 style="color: #FF6B6B;">📊 Top Skills by Frequency</h3>', unsafe_allow_html=True)

        skill_frequencies = analysis_service.analyze_skills_frequency(jobs)
        top_skills = skill_frequencies[:15]

        if top_skills:
            df_skills = pd.DataFrame(top_skills)

            fig = px.bar(
                df_skills,
                x="frequency",
                y="skill",
                orientation='h',
                title="Most In-Demand Skills",
                color="frequency",
                color_continuous_scale=[[0, '#4ECDC4'], [0.5, '#FFE66D'], [1, '#FF6B6B']]
            )
            fig.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                plot_bgcolor='#0a0a0a',
                paper_bgcolor='#0a0a0a',
                font=dict(size=14, family="Arial", color='white'),
                title_font_color='white'
            )
            fig.update_xaxes(gridcolor='#2a2a3e', showgrid=True, title_font_color='white', tickfont_color='white')
            fig.update_yaxes(gridcolor='#2a2a3e', showgrid=True, title_font_color='white', tickfont_color='white')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<h3 style="color: #FF8E53;">🔗 Skills Co-occurrence</h3>', unsafe_allow_html=True)

        skill_combinations = analysis_service.find_skill_combinations(jobs)
        top_combinations = skill_combinations[:10]

        if top_combinations:
            st.markdown("""
            <div class="featured-card" style="border-color: #FF8E53;">
                <h4 style="color: white; margin-bottom: 1rem;">Top skill combinations</h4>
            """, unsafe_allow_html=True)

            for combo in top_combinations:
                skills_str = " + ".join(combo["skills"])
                st.markdown(
                    f'<p style="color: #ffffff;">• <strong style="color: #FFE66D;">{skills_str}</strong> <span style="color: #4ECDC4;">({combo["frequency"]} jobs)</span></p>',
                    unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()