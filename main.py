# """
# Main Streamlit application for Resume Parser and Ranking System
# """

# import streamlit as st
# import os
# import json
# from pathlib import Path
# import pandas as pd
# from datetime import datetime
# import base64

# # Import our custom modules
# from resume_parser import ResumeParser
# from gemini_ranker import GeminiRanker
# from data_manager import DataManager
# from config import DATA_DIR, RESUMES_DIR, JSON_DIR, ALLOWED_EXTENSIONS

# # Page configuration
# st.set_page_config(
#     page_title="Resume Parser & Ranking System",
#     page_icon="📄",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         padding: 2rem 0;
#         text-align: center;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         margin: -1rem -1rem 2rem -1rem;
#         border-radius: 0.5rem;
#     }
#     .metric-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 0.5rem;
#         border-left: 4px solid #667eea;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#     }
#     .ranking-card {
#         border: 1px solid #e0e0e0;
#         border-radius: 0.5rem;
#         padding: 1rem;
#         margin: 0.5rem 0;
#         background: white;
#     }
#     .score-badge {
#         display: inline-block;
#         padding: 0.25rem 0.75rem;
#         border-radius: 1rem;
#         color: white;
#         font-weight: bold;
#         text-align: center;
#     }
#     .score-excellent { background-color: #28a745; }
#     .score-good { background-color: #17a2b8; }
#     .score-average { background-color: #ffc107; color: black; }
#     .score-poor { background-color: #dc3545; }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'parsed_resumes' not in st.session_state:
#     st.session_state.parsed_resumes = []
# if 'rankings' not in st.session_state:
#     st.session_state.rankings = []
# if 'gemini_api_key' not in st.session_state:
#     st.session_state.gemini_api_key = ""

# # Initialize components
# @st.cache_resource
# def initialize_components():
#     parser = ResumeParser()
#     data_manager = DataManager(JSON_DIR)
#     return parser, data_manager

# parser, data_manager = initialize_components()

# def get_score_badge_class(score):
#     """Get CSS class for score badge based on score value"""
#     if score >= 80:
#         return "score-excellent"
#     elif score >= 65:
#         return "score-good"
#     elif score >= 50:
#         return "score-average"
#     else:
#         return "score-poor"

# def main():
#     # Header
#     st.markdown("""
#     <div class="main-header">
#         <h1>🎯 Resume Parser & Ranking System</h1>
#         <p>Powered by AI for intelligent candidate matching</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar for navigation and settings
#     with st.sidebar:
#         st.image("https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg?auto=compress&cs=tinysrgb&w=300&h=200&fit=crop", 
#                  caption="AI-Powered Recruitment")
        
#         st.header("⚙️ Settings")
        
#         # Gemini API Key input
#         api_key = st.text_input(
#             "🔑 Gemini API Key",
#             type="password",
#             value=st.session_state.gemini_api_key,
#             help="Enter your Google Gemini API key for AI-powered ranking"
#         )
        
#         if api_key != st.session_state.gemini_api_key:
#             st.session_state.gemini_api_key = api_key
        
#         st.markdown("---")
        
#         # Navigation
#         st.header("🧭 Navigation")
#         page = st.selectbox(
#             "Select Page",
#             ["📤 Upload & Parse", "📊 View Parsed Resumes", "🎯 Job Matching & Ranking", "📈 Analytics"]
#         )
        
#         st.markdown("---")
        
#         # Quick stats
#         st.header("📋 Quick Stats")
#         existing_resumes = data_manager.load_all_resumes()
#         st.metric("Total Parsed Resumes", len(existing_resumes))
        
#         if existing_resumes:
#             avg_exp = sum(r.get('experience_years', 0) for r in existing_resumes) / len(existing_resumes)
#             st.metric("Average Experience", f"{avg_exp:.1f} years")
    
#     # Main content area
#     if page == "📤 Upload & Parse":
#         upload_and_parse_page()
#     elif page == "📊 View Parsed Resumes":
#         view_resumes_page()
#     elif page == "🎯 Job Matching & Ranking":
#         job_matching_page()
#     else:
#         analytics_page()

# def upload_and_parse_page():
#     st.header("📤 Upload & Parse Resumes")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.subheader("Upload Resume Files")
#         uploaded_files = st.file_uploader(
#             "Choose PDF or DOCX files",
#             type=['pdf', 'docx'],
#             accept_multiple_files=True,
#             help="Upload multiple resume files to parse them automatically"
#         )
        
#         if uploaded_files:
#             st.info(f"📁 {len(uploaded_files)} files selected for parsing")
            
#             if st.button("🚀 Start Parsing", type="primary"):
#                 progress_bar = st.progress(0)
#                 status_text = st.empty()
#                 results_container = st.empty()
                
#                 parsed_results = []
                
#                 for i, uploaded_file in enumerate(uploaded_files):
#                     status_text.text(f"Processing: {uploaded_file.name}")
                    
#                     # Save uploaded file temporarily
#                     temp_file_path = RESUMES_DIR / uploaded_file.name
#                     with open(temp_file_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
                    
#                     # Parse the resume
#                     parsed_data = parser.parse_resume(temp_file_path)
                    
#                     if parsed_data:
#                         # Save parsed data
#                         json_path = data_manager.save_resume_data(parsed_data)
#                         if json_path:
#                             parsed_results.append(parsed_data)
#                             st.success(f"✅ Parsed: {uploaded_file.name}")
#                         else:
#                             st.error(f"❌ Failed to save: {uploaded_file.name}")
#                     else:
#                         st.error(f"❌ Failed to parse: {uploaded_file.name}")
                    
#                     # Update progress
#                     progress_bar.progress((i + 1) / len(uploaded_files))
                
#                 status_text.text("✨ Parsing completed!")
                
#                 # Display results summary
#                 if parsed_results:
#                     st.success(f"🎉 Successfully parsed {len(parsed_results)} resumes!")
                    
#                     # Show quick preview of parsed data
#                     with st.expander("👀 Preview Parsed Data"):
#                         df = data_manager.create_dataframe(parsed_results)
#                         st.dataframe(df, use_container_width=True)
    
#     with col2:
#         st.subheader("📋 Parsing Guidelines")
#         st.markdown("""
#         **Supported Formats:**
#         - PDF files (*.pdf)
#         - Word documents (*.docx)
        
#         **Extracted Information:**
#         - 👤 Name and contact details
#         - 📧 Email address
#         - 📱 Phone number
#         - 💼 Work experience (years)
#         - 🛠️ Technical skills
#         - 🎓 Education background
        
#         **Tips for Better Results:**
#         - Use well-formatted resumes
#         - Ensure text is readable
#         - Include clear section headers
#         - Limit file size to 10MB
#         """)
        
#         # Show recent parsing activity
#         recent_resumes = data_manager.load_all_resumes()
#         if recent_resumes:
#             st.subheader("📚 Recently Parsed")
#             for resume in recent_resumes[-3:]:  # Show last 3
#                 with st.container():
#                     st.markdown(f"**{resume.get('name', 'Unknown')}**")
#                     st.caption(f"Skills: {len(resume.get('skills', []))} | Experience: {resume.get('experience_years', 0)} years")

# def view_resumes_page():
#     st.header("📊 View Parsed Resumes")
    
#     # Load all parsed resumes
#     all_resumes = data_manager.load_all_resumes()
    
#     if not all_resumes:
#         st.info("📭 No parsed resumes found. Please upload and parse some resumes first.")
#         return
    
#     # Statistics overview
#     stats = data_manager.get_statistics(all_resumes)
    
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.metric("📄 Total Resumes", stats.get('total_resumes', 0))
#     with col2:
#         st.metric("📊 Avg Experience", f"{stats.get('average_experience', 0)} years")
#     with col3:
#         exp_range = stats.get('experience_range', {})
#         st.metric("📈 Experience Range", f"{exp_range.get('min', 0)}-{exp_range.get('max', 0)} years")
#     with col4:
#         top_skills = stats.get('top_skills', [])
#         most_common_skill = top_skills[0][0] if top_skills else "N/A"
#         st.metric("🔥 Top Skill", most_common_skill)
    
#     # Filters
#     st.subheader("🔍 Filter Options")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         min_experience = st.number_input("Min Experience (years)", min_value=0, max_value=50, value=0)
#     with col2:
#         max_experience = st.number_input("Max Experience (years)", min_value=0, max_value=50, value=50)
#     with col3:
#         skill_filter = st.text_input("Filter by Skill", placeholder="e.g., Python, Java")
    
#     # Apply filters
#     filtered_resumes = []
#     for resume in all_resumes:
#         exp_years = resume.get('experience_years', 0)
#         skills = [s.lower() for s in resume.get('skills', [])]
        
#         # Check experience filter
#         if not (min_experience <= exp_years <= max_experience):
#             continue
        
#         # Check skill filter
#         if skill_filter and skill_filter.lower() not in ' '.join(skills):
#             continue
        
#         filtered_resumes.append(resume)
    
#     st.info(f"📋 Showing {len(filtered_resumes)} of {len(all_resumes)} resumes")
    
#     # Display resumes
#     if filtered_resumes:
#         # Create DataFrame
#         df = data_manager.create_dataframe(filtered_resumes)
        
#         # Display options
#         view_option = st.selectbox("📊 View Style", ["Table View", "Card View"])
        
#         if view_option == "Table View":
#             st.dataframe(
#                 df,
#                 use_container_width=True,
#                 column_config={
#                     "Skills": st.column_config.TextColumn(width="medium"),
#                     "Education": st.column_config.TextColumn(width="medium")
#                 }
#             )
#         else:
#             # Card view
#             for i, resume in enumerate(filtered_resumes):
#                 with st.expander(f"👤 {resume.get('name', 'Unknown')} - {resume.get('experience_years', 0)} years exp"):
#                     col1, col2 = st.columns([2, 1])
                    
#                     with col1:
#                         st.write(f"**📧 Email:** {resume.get('email', 'N/A')}")
#                         st.write(f"**📱 Phone:** {resume.get('phone', 'N/A')}")
#                         st.write(f"**💼 Experience:** {resume.get('experience_years', 0)} years")
#                         st.write(f"**🎓 Education:** {', '.join(resume.get('education', ['N/A']))}")
                    
#                     with col2:
#                         st.write("**🛠️ Skills:**")
#                         skills = resume.get('skills', [])
#                         for skill in skills[:10]:  # Show first 10 skills
#                             st.badge(skill)
#                         if len(skills) > 10:
#                             st.caption(f"... and {len(skills) - 10} more")
        
#         # Export option
#         if st.button("📥 Export to CSV"):
#             csv_path = data_manager.export_rankings_to_csv(
#                 [{'candidate_name': r.get('name'), 'candidate_email': r.get('email'), 
#                   'experience_years': r.get('experience_years'), 'match_score': 'N/A',
#                   'strengths': ', '.join(r.get('skills', [])), 'weaknesses': 'N/A',
#                   'file_name': r.get('file_name')} for r in filtered_resumes],
#                 f"parsed_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
#             )
#             if csv_path:
#                 st.success(f"📊 Data exported to: {csv_path}")

# def job_matching_page():
#     st.header("🎯 Job Matching & Ranking")
    
#     if not st.session_state.gemini_api_key:
#         st.warning("⚠️ Please enter your Gemini API key in the sidebar to use AI ranking features.")
#         return
    
#     # Load all parsed resumes
#     all_resumes = data_manager.load_all_resumes()
    
#     if not all_resumes:
#         st.info("📭 No parsed resumes found. Please upload and parse some resumes first.")
#         return
    
#     st.info(f"📊 Found {len(all_resumes)} parsed resumes ready for ranking")
    
#     # Job description input
#     st.subheader("📝 Job Description")
#     job_description = st.text_area(
#         "Enter the job description to match candidates against:",
#         height=200,
#         placeholder="""Example:
# We are looking for a Senior Python Developer with 3+ years of experience.
# The ideal candidate should have:
# - Strong Python programming skills
# - Experience with Django/Flask frameworks
# - Knowledge of SQL databases
# - Experience with cloud platforms (AWS/GCP)
# - Bachelor's degree in Computer Science or related field
# """
#     )
    
#     if not job_description.strip():
#         st.warning("⚠️ Please enter a job description to proceed with ranking.")
#         return
    
#     # Ranking options
#     col1, col2 = st.columns(2)
#     with col1:
#         max_candidates = st.number_input(
#             "Maximum candidates to rank",
#             min_value=1,
#             max_value=len(all_resumes),
#             value=min(20, len(all_resumes))
#         )
    
#     with col2:
#         include_summary = st.checkbox("Include AI Summary Report", value=True)
    
#     # Start ranking
#     if st.button("🚀 Start AI Ranking", type="primary"):
#         try:
#             # Initialize Gemini ranker
#             ranker = GeminiRanker(st.session_state.gemini_api_key)
            
#             with st.spinner("🤖 AI is analyzing and ranking candidates..."):
#                 # Limit candidates if requested
#                 candidates_to_rank = all_resumes[:max_candidates]
                
#                 # Get rankings
#                 rankings = ranker.rank_all_candidates(job_description, candidates_to_rank)
                
#                 # Store in session state
#                 st.session_state.rankings = rankings
            
#             st.success(f"✅ Successfully ranked {len(rankings)} candidates!")
            
#             # Display results
#             display_ranking_results(rankings, job_description, include_summary, ranker)
            
#         except Exception as e:
#             st.error(f"❌ Error during ranking: {str(e)}")
#             st.info("💡 Please check your Gemini API key and ensure you have sufficient quota.")

# def display_ranking_results(rankings, job_description, include_summary, ranker):
#     """Display ranking results in a formatted way"""
    
#     if include_summary:
#         st.subheader("📋 Executive Summary")
#         with st.spinner("Generating summary..."):
#             summary = ranker.generate_summary_report(rankings, job_description)
#             st.info(summary)
    
#     st.subheader("🏆 Candidate Rankings")
    
#     # Top candidates overview
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("🥇 Top Score", f"{rankings[0].get('match_score', 0)}%")
#     with col2:
#         avg_score = sum(r.get('match_score', 0) for r in rankings) / len(rankings)
#         st.metric("📊 Average Score", f"{avg_score:.1f}%")
#     with col3:
#         qualified_candidates = sum(1 for r in rankings if r.get('match_score', 0) >= 70)
#         st.metric("✅ Qualified (70%+)", qualified_candidates)
    
#     # Detailed rankings
#     for i, candidate in enumerate(rankings, 1):
#         score = candidate.get('match_score', 0)
#         score_class = get_score_badge_class(score)
        
#         with st.expander(f"#{i} {candidate.get('candidate_name', 'Unknown')} - {score}% match"):
#             col1, col2 = st.columns([2, 1])
            
#             with col1:
#                 st.markdown(f"**📧 Email:** {candidate.get('candidate_email', 'N/A')}")
#                 st.markdown(f"**💼 Experience:** {candidate.get('experience_years', 0)} years")
#                 st.markdown(f"**📁 File:** {candidate.get('file_name', 'N/A')}")
                
#                 st.markdown("**🎯 AI Explanation:**")
#                 st.write(candidate.get('explanation', 'No explanation provided'))
            
#             with col2:
#                 st.markdown(f'<div class="score-badge {score_class}">{score}% Match</div>', unsafe_allow_html=True)
                
#                 st.markdown("**💪 Strengths:**")
#                 for strength in candidate.get('strengths', []):
#                     st.write(f"• {strength}")
                
#                 st.markdown("**⚠️ Areas of Concern:**")
#                 for weakness in candidate.get('weaknesses', []):
#                     st.write(f"• {weakness}")
    
#     # Export rankings
#     if st.button("📥 Export Rankings to CSV"):
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         csv_path = data_manager.export_rankings_to_csv(rankings, f"candidate_rankings_{timestamp}")
#         if csv_path:
#             st.success(f"📊 Rankings exported to: {csv_path}")

# def analytics_page():
#     st.header("📈 Analytics Dashboard")
    
#     all_resumes = data_manager.load_all_resumes()
    
#     if not all_resumes:
#         st.info("📭 No data available for analytics. Please parse some resumes first.")
#         return
    
#     # Overall statistics
#     stats = data_manager.get_statistics(all_resumes)
    
#     st.subheader("📊 Overview Statistics")
    
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.metric("📄 Total Resumes", stats.get('total_resumes', 0))
#     with col2:
#         st.metric("📊 Avg Experience", f"{stats.get('average_experience', 0):.1f} years")
#     with col3:
#         exp_range = stats.get('experience_range', {})
#         st.metric("🔻 Min Experience", f"{exp_range.get('min', 0)} years")
#     with col4:
#         st.metric("🔺 Max Experience", f"{exp_range.get('max', 0)} years")
    
#     # Skills analysis
#     st.subheader("🛠️ Skills Analysis")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.write("**Top 10 Most Common Skills:**")
#         top_skills = stats.get('top_skills', [])
        
#         if top_skills:
#             skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
#             st.bar_chart(skills_df.set_index('Skill')['Count'])
#         else:
#             st.info("No skills data available")
    
#     with col2:
#         st.write("**Experience Distribution:**")
#         exp_years = [r.get('experience_years', 0) for r in all_resumes]
#         exp_df = pd.DataFrame({'Experience': exp_years})
#         st.histogram(exp_df['Experience'], bins=10)
    
#     # Recent activity
#     st.subheader("📅 Recent Activity")
    
#     # Sort resumes by parsed date
#     sorted_resumes = sorted(
#         all_resumes,
#         key=lambda x: x.get('parsed_date', ''),
#         reverse=True
#     )
    
#     recent_activity = []
#     for resume in sorted_resumes[:10]:  # Last 10 activities
#         recent_activity.append({
#             'Date': resume.get('parsed_date', 'N/A')[:10],  # Just the date part
#             'Name': resume.get('name', 'Unknown'),
#             'Skills Count': len(resume.get('skills', [])),
#             'Experience': f"{resume.get('experience_years', 0)} years"
#         })
    
#     if recent_activity:
#         recent_df = pd.DataFrame(recent_activity)
#         st.dataframe(recent_df, use_container_width=True)
    
#     # Rankings analysis (if available)
#     if st.session_state.rankings:
#         st.subheader("🎯 Latest Ranking Analysis")
#         rankings = st.session_state.rankings
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             scores = [r.get('match_score', 0) for r in rankings]
#             scores_df = pd.DataFrame({'Scores': scores})
#             st.write("**Match Score Distribution:**")
#             st.histogram(scores_df['Scores'], bins=10)
        
#         with col2:
#             # Top performers
#             st.write("**Top 5 Performers:**")
#             for i, candidate in enumerate(rankings[:5], 1):
#                 score = candidate.get('match_score', 0)
#                 name = candidate.get('candidate_name', 'Unknown')
#                 st.write(f"{i}. {name}: {score}%")

# if __name__ == "__main__":
#     main()

"""
Main Streamlit application for Resume Parser and Ranking System
"""

import streamlit as st
import os
import json
from pathlib import Path
import pandas as pd
from datetime import datetime
import base64
import tempfile

# Import our custom modules
from resume_parser import ResumeParser
from gemini_ranker import GeminiRanker
from data_manager import DataManager
from config import ALLOWED_EXTENSIONS, GEMINI_API_KEY_DIRECT

# Page configuration
st.set_page_config(
    page_title="Resume Parser & Ranking System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        padding: 2rem 0;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0.5rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .ranking-card {
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
    }
    .score-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    .score-excellent { background-color: #28a745; }
    .score-good { background-color: #17a2b8; }
    .score-average { background-color: #ffc107; color: black; }
    .score-poor { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'parsed_resumes' not in st.session_state:
    st.session_state.parsed_resumes = []
if 'rankings' not in st.session_state:
    st.session_state.rankings = []
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = GEMINI_API_KEY_DIRECT

# Initialize components
def initialize_components(api_key):
    parser = ResumeParser(api_key)
    data_manager = DataManager()
    return parser, data_manager

def get_score_badge_class(score):
    """Get CSS class for score badge based on score value"""
    if score >= 80:
        return "score-excellent"
    elif score >= 65:
        return "score-good"
    elif score >= 50:
        return "score-average"
    else:
        return "score-poor"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Resume Parser & Ranking System</h1>
        <p>Powered by AI for intelligent candidate matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.image("https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg?auto=compress&cs=tinysrgb&w=300&h=200&fit=crop", 
                 caption="AI-Powered Recruitment")
        
        st.header("⚙️ Settings")
        
        # Gemini API Key input
        api_key = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            value=st.session_state.gemini_api_key,
            help="Enter your Google Gemini API key for AI-powered parsing and ranking"
        )
        
        if api_key != st.session_state.gemini_api_key:
            st.session_state.gemini_api_key = api_key
        
        st.markdown("---")
        
        # Navigation
        st.header("🧭 Navigation")
        page = st.selectbox(
            "Select Page",
            ["📤 Upload & Parse", "📊 View Parsed Resumes", "🎯 Job Matching & Ranking", "📈 Analytics", "🛠️ Data Management"]
        )
        
        st.markdown("---")
        
        # Quick stats
        data_manager = DataManager()
        existing_resumes = data_manager.load_all_resumes()
        st.metric("Total Parsed Resumes", len(existing_resumes))
        
        if existing_resumes:
            avg_exp = sum(r.get('experience_years', 0) for r in existing_resumes) / len(existing_resumes)
            st.metric("Average Experience", f"{avg_exp:.1f} years")
    
    # Main content area
    if not st.session_state.gemini_api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to use all features.")
        return
    
    # Initialize components with API key
    parser, data_manager = initialize_components(st.session_state.gemini_api_key)
    
    if page == "📤 Upload & Parse":
        upload_and_parse_page(parser, data_manager)
    elif page == "📊 View Parsed Resumes":
        view_resumes_page(data_manager)
    elif page == "🎯 Job Matching & Ranking":
        job_matching_page(data_manager)
    elif page == "📈 Analytics":
        analytics_page(data_manager)
    else:
        data_management_page(data_manager)

def upload_and_parse_page(parser, data_manager):
    st.header("📤 Upload & Parse Resumes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Resume Files")
        uploaded_files = st.file_uploader(
            "Choose PDF, DOCX or TXT files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload multiple resume files to parse them automatically"
        )
        
        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} files selected for parsing")
            
            if st.button("🚀 Start Parsing", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                parsed_results = []
                failed_files = []
                
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Processing: {uploaded_file.name}")
                    
                    # Save uploaded file to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        temp_file_path = tmp_file.name
                    
                    # Parse the resume
                    parsed_data = parser.parse_resume(temp_file_path)
                    
                    # Clean up temporary file
                    os.unlink(temp_file_path)
                    
                    if parsed_data:
                        # Save parsed data
                        result = data_manager.save_resume_data(parsed_data)
                        if result:
                            parsed_results.append(parsed_data)
                            st.success(f"✅ Parsed: {uploaded_file.name}")
                        else:
                            st.error(f"❌ Failed to save: {uploaded_file.name}")
                            failed_files.append(uploaded_file.name)
                    else:
                        st.error(f"❌ Failed to parse: {uploaded_file.name}")
                        failed_files.append(uploaded_file.name)
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.text("✨ Parsing completed!")
                
                # Display results summary
                if parsed_results:
                    st.success(f"🎉 Successfully parsed {len(parsed_results)} resumes!")
                    
                    # Show quick preview of parsed data
                    with st.expander("👀 Preview Parsed Data"):
                        df = data_manager.create_dataframe(parsed_results)
                        st.dataframe(df, use_container_width=True)
                
                if failed_files:
                    st.error(f"❌ Failed to parse {len(failed_files)} files: {', '.join(failed_files)}")
    
    with col2:
        st.subheader("📋 Parsing Guidelines")
        st.markdown("""
        **Supported Formats:**
        - PDF files (*.pdf)
        - Word documents (*.docx)
        - Text files (*.txt)
        
        **Extracted Information:**
        - 👤 Name and contact details
        - 📧 Email address
        - 📱 Phone number
        - 💼 Work experience (years)
        - 🛠️ Technical skills
        - 🎓 Education background
        - 📝 Professional summary
        
        **Tips for Better Results:**
        - Use well-formatted resumes
        - Ensure text is readable
        - Include clear section headers
        - Limit file size to 10MB
        """)
        
        # Show recent parsing activity
        recent_resumes = data_manager.load_all_resumes()
        if recent_resumes:
            st.subheader("📚 Recently Parsed")
            for resume in recent_resumes[-3:]:  # Show last 3
                with st.container():
                    st.markdown(f"**{resume.get('name', 'Unknown')}**")
                    st.caption(f"Skills: {len(resume.get('skills', []))} | Experience: {resume.get('experience_years', 0)} years")

def view_resumes_page(data_manager):
    st.header("📊 View Parsed Resumes")
    
    # Load all parsed resumes
    all_resumes = data_manager.load_all_resumes()
    
    if not all_resumes:
        st.info("📭 No parsed resumes found. Please upload and parse some resumes first.")
        return
    
    # Statistics overview
    stats = data_manager.get_statistics(all_resumes)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Total Resumes", stats.get('total_resumes', 0))
    with col2:
        st.metric("📊 Avg Experience", f"{stats.get('average_experience', 0)} years")
    with col3:
        exp_range = stats.get('experience_range', {})
        st.metric("📈 Experience Range", f"{exp_range.get('min', 0)}-{exp_range.get('max', 0)} years")
    with col4:
        top_skills = stats.get('top_skills', [])
        most_common_skill = top_skills[0][0] if top_skills else "N/A"
        st.metric("🔥 Top Skill", most_common_skill)
    
    # Filters
    st.subheader("🔍 Filter Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_experience = st.number_input("Min Experience (years)", min_value=0, max_value=50, value=0)
    with col2:
        max_experience = st.number_input("Max Experience (years)", min_value=0, max_value=50, value=50)
    with col3:
        skill_filter = st.text_input("Filter by Skill", placeholder="e.g., Python, Java")
    
    # Apply filters
    filtered_resumes = []
    for resume in all_resumes:
        exp_years = resume.get('experience_years', 0)
        skills = [s.lower() for s in resume.get('skills', [])]
        
        # Check experience filter
        if not (min_experience <= exp_years <= max_experience):
            continue
        
        # Check skill filter
        if skill_filter and skill_filter.lower() not in ' '.join(skills):
            continue
        
        filtered_resumes.append(resume)
    
    st.info(f"📋 Showing {len(filtered_resumes)} of {len(all_resumes)} resumes")
    
    # Display resumes
    if filtered_resumes:
        # Create DataFrame
        df = data_manager.create_dataframe(filtered_resumes)
        
        # Display options
        view_option = st.selectbox("📊 View Style", ["Table View", "Card View", "Raw JSON View"])
        
        if view_option == "Table View":
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Skills": st.column_config.TextColumn(width="medium"),
                    "Education": st.column_config.TextColumn(width="medium"),
                    "Summary": st.column_config.TextColumn(width="large")
                }
            )
        elif view_option == "Card View":
            # Card view
            for i, resume in enumerate(filtered_resumes):
                with st.expander(f"👤 {resume.get('name', 'Unknown')} - {resume.get('experience_years', 0)} years exp"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**📧 Email:** {resume.get('email', 'N/A')}")
                        st.write(f"**📱 Phone:** {resume.get('phone', 'N/A')}")
                        st.write(f"**💼 Experience:** {resume.get('experience_years', 0)} years")
                        st.write(f"**🎓 Education:** {', '.join(resume.get('education', ['N/A']))}")
                        st.write(f"**📝 Summary:** {resume.get('summary', 'N/A')}")
                    
                    with col2:
                        st.write("**🛠️ Skills:**")
                        skills = resume.get('skills', [])
                        for skill in skills[:10]:  # Show first 10 skills
                            st.badge(skill)
                        if len(skills) > 10:
                            st.caption(f"... and {len(skills) - 10} more")
        else:
            # Raw JSON view
            selected_resume = st.selectbox("Select Resume", options=[r.get('name', 'Unknown') for r in filtered_resumes])
            selected_data = next((r for r in filtered_resumes if r.get('name') == selected_resume), None)
            if selected_data:
                st.json(selected_data)
        
        # Export option
        csv_data = data_manager.export_resumes_to_csv(filtered_resumes)
        if csv_data:
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"parsed_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )

def job_matching_page(data_manager):
    st.header("🎯 Job Matching & Ranking")
    
    # Load all parsed resumes
    all_resumes = data_manager.load_all_resumes()
    
    if not all_resumes:
        st.info("📭 No parsed resumes found. Please upload and parse some resumes first.")
        return
    
    st.info(f"📊 Found {len(all_resumes)} parsed resumes ready for ranking")
    
    # Job description input
    st.subheader("📝 Job Description")
    job_description = st.text_area(
        "Enter the job description to match candidates against:",
        height=200,
        placeholder="""Example:
We are looking for a Senior Python Developer with 3+ years of experience.
The ideal candidate should have:
- Strong Python programming skills
- Experience with Django/Flask frameworks
- Knowledge of SQL databases
- Experience with cloud platforms (AWS/GCP)
- Bachelor's degree in Computer Science or related field
"""
    )
    
    if not job_description.strip():
        st.warning("⚠️ Please enter a job description to proceed with ranking.")
        return
    
    # Ranking options
    col1, col2 = st.columns(2)
    with col1:
        max_candidates = st.number_input(
            "Maximum candidates to rank",
            min_value=1,
            max_value=len(all_resumes),
            value=min(20, len(all_resumes))
        )
    
    with col2:
        include_summary = st.checkbox("Include AI Summary Report", value=True)
    
    # Start ranking
    if st.button("🚀 Start AI Ranking", type="primary"):
        try:
            # Initialize Gemini ranker
            ranker = GeminiRanker(st.session_state.gemini_api_key)
            
            with st.spinner("🤖 AI is analyzing and ranking candidates..."):
                # Limit candidates if requested
                candidates_to_rank = all_resumes[:max_candidates]
                
                # Get rankings
                rankings = ranker.rank_all_candidates(job_description, candidates_to_rank)
                
                # Store in session state
                st.session_state.rankings = rankings
            
            st.success(f"✅ Successfully ranked {len(rankings)} candidates!")
            
            # Display results
            display_ranking_results(rankings, job_description, include_summary, ranker, data_manager)
            
        except Exception as e:
            st.error(f"❌ Error during ranking: {str(e)}")
            st.info("💡 Please check your Gemini API key and ensure you have sufficient quota.")

def display_ranking_results(rankings, job_description, include_summary, ranker, data_manager):
    """Display ranking results in a formatted way"""
    
    if include_summary:
        st.subheader("📋 Executive Summary")
        with st.spinner("Generating summary..."):
            summary = ranker.generate_summary_report(rankings, job_description)
            st.info(summary)
    
    st.subheader("🏆 Candidate Rankings")
    
    # Top candidates overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🥇 Top Score", f"{rankings[0].get('match_score', 0)}%")
    with col2:
        avg_score = sum(r.get('match_score', 0) for r in rankings) / len(rankings)
        st.metric("📊 Average Score", f"{avg_score:.1f}%")
    with col3:
        qualified_candidates = sum(1 for r in rankings if r.get('match_score', 0) >= 70)
        st.metric("✅ Qualified (70%+)", qualified_candidates)
    
    # Detailed rankings
    for i, candidate in enumerate(rankings, 1):
        score = candidate.get('match_score', 0)
        score_class = get_score_badge_class(score)
        
        with st.expander(f"#{i} {candidate.get('candidate_name', 'Unknown')} - {score}% match"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📧 Email:** {candidate.get('candidate_email', 'N/A')}")
                st.markdown(f"**💼 Experience:** {candidate.get('experience_years', 0)} years")
                st.markdown(f"**📁 File:** {candidate.get('file_name', 'N/A')}")
                
                st.markdown("**🎯 AI Explanation:**")
                st.write(candidate.get('explanation', 'No explanation provided'))
            
            with col2:
                st.markdown(f'<div class="score-badge {score_class}">{score}% Match</div>', unsafe_allow_html=True)
                
                st.markdown("**💪 Strengths:**")
                for strength in candidate.get('strengths', []):
                    st.write(f"• {strength}")
                
                st.markdown("**⚠️ Areas of Concern:**")
                for weakness in candidate.get('weaknesses', []):
                    st.write(f"• {weakness}")
    
    # Export rankings
    csv_data = data_manager.export_rankings_to_csv(rankings)
    if csv_data:
        st.download_button(
            label="📥 Download Rankings CSV",
            data=csv_data,
            file_name=f"candidate_rankings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

def analytics_page(data_manager):
    st.header("📈 Analytics Dashboard")
    
    all_resumes = data_manager.load_all_resumes()
    
    if not all_resumes:
        st.info("📭 No data available for analytics. Please parse some resumes first.")
        return
    
    # Overall statistics
    stats = data_manager.get_statistics(all_resumes)
    
    st.subheader("📊 Overview Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Total Resumes", stats.get('total_resumes', 0))
    with col2:
        st.metric("📊 Avg Experience", f"{stats.get('average_experience', 0):.1f} years")
    with col3:
        exp_range = stats.get('experience_range', {})
        st.metric("🔻 Min Experience", f"{exp_range.get('min', 0)} years")
    with col4:
        st.metric("🔺 Max Experience", f"{exp_range.get('max', 0)} years")
    
    # Skills analysis
    st.subheader("🛠️ Skills Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 10 Most Common Skills:**")
        top_skills = stats.get('top_skills', [])
        
        if top_skills:
            skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
            st.bar_chart(skills_df.set_index('Skill')['Count'])
        else:
            st.info("No skills data available")
    
    with col2:
        st.write("**Experience Distribution:**")
        exp_years = [r.get('experience_years', 0) for r in all_resumes]
        exp_df = pd.DataFrame({'Experience': exp_years})
        st.histogram(exp_df['Experience'], bins=10)
    
    # Recent activity
    st.subheader("📅 Recent Activity")
    
    # Sort resumes by parsed date
    sorted_resumes = sorted(
        all_resumes,
        key=lambda x: x.get('parsed_date', ''),
        reverse=True
    )
    
    recent_activity = []
    for resume in sorted_resumes[:10]:  # Last 10 activities
        recent_activity.append({
            'Date': resume.get('parsed_date', 'N/A')[:10],  # Just the date part
            'Name': resume.get('name', 'Unknown'),
            'Skills Count': len(resume.get('skills', [])),
            'Experience': f"{resume.get('experience_years', 0)} years"
        })
    
    if recent_activity:
        recent_df = pd.DataFrame(recent_activity)
        st.dataframe(recent_df, use_container_width=True)
    
    # Rankings analysis (if available)
    if st.session_state.rankings:
        st.subheader("🎯 Latest Ranking Analysis")
        rankings = st.session_state.rankings
        
        col1, col2 = st.columns(2)
        
        with col1:
            scores = [r.get('match_score', 0) for r in rankings]
            scores_df = pd.DataFrame({'Scores': scores})
            st.write("**Match Score Distribution:**")
            st.histogram(scores_df['Scores'], bins=10)
        
        with col2:
            # Top performers
            st.write("**Top 5 Performers:**")
            for i, candidate in enumerate(rankings[:5], 1):
                score = candidate.get('match_score', 0)
                name = candidate.get('candidate_name', 'Unknown')
                st.write(f"{i}. {name}: {score}%")

def data_management_page(data_manager):
    st.header("🛠️ Data Management")

    all_resumes = data_manager.load_all_resumes()

    if not all_resumes:
        st.info("📭 No parsed resumes found.")
        return

    st.info(f"📊 Found {len(all_resumes)} parsed resumes in the system")

    # Export all data
    st.subheader("📥 Export Data")
    csv_data = data_manager.export_resumes_to_csv(all_resumes)
    if csv_data:
        st.download_button(
            label="Download All Resumes as CSV",
            data=csv_data,
            file_name=f"all_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    
    # Individual resume management
    st.subheader("📄 Manage Individual Resumes")
    
    if all_resumes:
        # Create a list of resume names for selection
        resume_options = [f"{i+1}. {r.get('name', 'Unknown')} - {r.get('file_name', '')}" 
                         for i, r in enumerate(all_resumes)]
        
        selected_indices = st.multiselect(
            "Select resumes to delete:",
            options=resume_options,
            format_func=lambda x: x
        )
        
        # Extract indices from selection
        indices_to_delete = [resume_options.index(opt) for opt in selected_indices]
        
        if indices_to_delete and st.button("🗑️ Delete Selected Resumes", type="secondary"):
            if data_manager.bulk_delete_resumes(indices_to_delete):
                st.success("✅ Selected resumes deleted successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to delete selected resumes")
    
    # Clear all data
    st.subheader("🗑️ Clear All Data")
    if st.button("Clear ALL Resume Data", type="primary"):
        if st.checkbox("⚠️ I understand this will permanently delete ALL parsed resumes"):
            if data_manager.clear_all_data():
                st.success("✅ All resume data cleared successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to clear data")


if __name__ == "__main__":
    main()