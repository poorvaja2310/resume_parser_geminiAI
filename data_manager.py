# """
# Data management functionality for storing and retrieving parsed resumes
# """

# import json
# import os
# from pathlib import Path
# from typing import List, Dict
# import pandas as pd
# from datetime import datetime

# class DataManager:
#     def __init__(self, json_dir: Path):
#         self.json_dir = Path(json_dir)
#         self.json_dir.mkdir(exist_ok=True)
    
#     def save_resume_data(self, resume_data: Dict, filename: str = None) -> Path:
#         """Save resume data to JSON file"""
#         if not filename:
#             name = resume_data.get('name', 'unknown').replace(' ', '_')
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = f"{name}_{timestamp}.json"
        
#         file_path = self.json_dir / filename
        
#         try:
#             with open(file_path, 'w', encoding='utf-8') as f:
#                 json.dump(resume_data, f, indent=2, ensure_ascii=False)
#             return file_path
#         except Exception as e:
#             print(f"Error saving resume data: {e}")
#             return None
    
#     def load_resume_data(self, filename: str) -> Dict:
#         """Load resume data from JSON file"""
#         file_path = self.json_dir / filename
        
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         except Exception as e:
#             print(f"Error loading resume data from {filename}: {e}")
#             return {}
    
#     def load_all_resumes(self) -> List[Dict]:
#         """Load all parsed resume data"""
#         resumes = []
        
#         for json_file in self.json_dir.glob('*.json'):
#             resume_data = self.load_resume_data(json_file.name)
#             if resume_data:
#                 resumes.append(resume_data)
        
#         return resumes
    
#     def get_resume_files_list(self) -> List[str]:
#         """Get list of all JSON resume files"""
#         return [f.name for f in self.json_dir.glob('*.json')]
    
#     def delete_resume_data(self, filename: str) -> bool:
#         """Delete a resume data file"""
#         file_path = self.json_dir / filename
        
#         try:
#             if file_path.exists():
#                 file_path.unlink()
#                 return True
#             return False
#         except Exception as e:
#             print(f"Error deleting resume data {filename}: {e}")
#             return False
    
#     def create_dataframe(self, resumes: List[Dict]) -> pd.DataFrame:
#         """Create pandas DataFrame from resume data"""
#         if not resumes:
#             return pd.DataFrame()
        
#         # Flatten the data for better table display
#         flattened_data = []
        
#         for resume in resumes:
#             flattened_resume = {
#                 'Name': resume.get('name', 'N/A'),
#                 'Email': resume.get('email', 'N/A'),
#                 'Phone': resume.get('phone', 'N/A'),
#                 'Experience (Years)': resume.get('experience_years', 0),
#                 'Skills Count': len(resume.get('skills', [])),
#                 'Skills': ', '.join(resume.get('skills', [])[:5]),  # Show first 5 skills
#                 'Education': ', '.join(resume.get('education', [])),
#                 'File Name': resume.get('file_name', 'N/A'),
#                 'Parsed Date': resume.get('parsed_date', 'N/A')
#             }
#             flattened_data.append(flattened_resume)
        
#         return pd.DataFrame(flattened_data)
    
#     def create_ranking_dataframe(self, rankings: List[Dict]) -> pd.DataFrame:
#         """Create pandas DataFrame from ranking data"""
#         if not rankings:
#             return pd.DataFrame()
        
#         ranking_data = []
        
#         for rank, candidate in enumerate(rankings, 1):
#             ranking_row = {
#                 'Rank': rank,
#                 'Name': candidate.get('candidate_name', 'N/A'),
#                 'Email': candidate.get('candidate_email', 'N/A'),
#                 'Match Score': candidate.get('match_score', 0),
#                 'Experience': candidate.get('experience_years', 0),
#                 'Strengths': ', '.join(candidate.get('strengths', [])),
#                 'Weaknesses': ', '.join(candidate.get('weaknesses', [])),
#                 'File Name': candidate.get('file_name', 'N/A')
#             }
#             ranking_data.append(ranking_row)
        
#         return pd.DataFrame(ranking_data)
    
#     def export_rankings_to_csv(self, rankings: List[Dict], filename: str) -> Path:
#         """Export rankings to CSV file"""
#         df = self.create_ranking_dataframe(rankings)
#         csv_path = self.json_dir.parent / f"{filename}.csv"
        
#         try:
#             df.to_csv(csv_path, index=False)
#             return csv_path
#         except Exception as e:
#             print(f"Error exporting rankings to CSV: {e}")
#             return None
    
#     def get_statistics(self, resumes: List[Dict]) -> Dict:
#         """Get statistics about the parsed resumes"""
#         if not resumes:
#             return {}
        
#         total_resumes = len(resumes)
        
#         # Calculate experience distribution
#         experience_years = [r.get('experience_years', 0) for r in resumes]
#         avg_experience = sum(experience_years) / len(experience_years)
        
#         # Count skills frequency
#         all_skills = []
#         for resume in resumes:
#             all_skills.extend(resume.get('skills', []))
        
#         skill_counts = {}
#         for skill in all_skills:
#             skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
#         top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
#         return {
#             'total_resumes': total_resumes,
#             'average_experience': round(avg_experience, 1),
#             'top_skills': top_skills,
#             'experience_range': {
#                 'min': min(experience_years),
#                 'max': max(experience_years)
#             }
#         }

"""
Data management functionality for storing and retrieving parsed resumes
"""

import json
from pathlib import Path
from typing import List, Dict
import pandas as pd
from datetime import datetime
import streamlit as st

class DataManager:
    def __init__(self):
        """Initialize data manager using session state for storage"""
        if 'resumes' not in st.session_state:
            st.session_state.resumes = []
    
    # ---------------- Save & Load ---------------- #
    def save_resume_data(self, resume_data: Dict) -> str:
        """Save resume data to session state"""
        try:
            # Add timestamp if not present
            if 'parsed_date' not in resume_data:
                resume_data['parsed_date'] = datetime.now().isoformat()
            
            # Add to session state
            st.session_state.resumes.append(resume_data)
            return "success"
        except Exception as e:
            print(f"Error saving resume data: {e}")
            return None

    def load_all_resumes(self) -> List[Dict]:
        """Load all parsed resume data from session state"""
        return st.session_state.resumes

    def clear_all_data(self) -> bool:
        """Clear all parsed resume data from session state"""
        try:
            st.session_state.resumes = []
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False

    def delete_resume_data(self, index: int) -> bool:
        """Delete a resume data by index"""
        try:
            if 0 <= index < len(st.session_state.resumes):
                st.session_state.resumes.pop(index)
                return True
            return False
        except Exception as e:
            print(f"Error deleting resume data: {e}")
            return False

    def bulk_delete_resumes(self, indices: List[int]) -> bool:
        """Delete multiple resumes by indices"""
        try:
            # Sort in reverse order to avoid index issues
            for index in sorted(indices, reverse=True):
                if 0 <= index < len(st.session_state.resumes):
                    st.session_state.resumes.pop(index)
            return True
        except Exception as e:
            print(f"Error in bulk delete: {e}")
            return False

    # ---------------- DataFrame Creation ---------------- #
    def create_dataframe(self, resumes: List[Dict]) -> pd.DataFrame:
        """Create pandas DataFrame from resume data"""
        if not resumes:
            return pd.DataFrame()

        flattened_data = []
        for resume in resumes:
            flattened_resume = {
                'Name': resume.get('name', 'N/A'),
                'Email': resume.get('email', 'N/A'),
                'Phone': resume.get('phone', 'N/A'),
                'Experience (Years)': resume.get('experience_years', 0),
                'Skills Count': len(resume.get('skills', [])),
                'Skills': ', '.join(resume.get('skills', [])[:5]),
                'Education': ', '.join(resume.get('education', [])),
                'Summary': resume.get('summary', 'N/A')[:100] + '...' if resume.get('summary') else 'N/A',
                'File Name': resume.get('file_name', 'N/A'),
                'Parsed Date': resume.get('parsed_date', 'N/A')
            }
            flattened_data.append(flattened_resume)
        return pd.DataFrame(flattened_data)

    def create_ranking_dataframe(self, rankings: List[Dict]) -> pd.DataFrame:
        """Create pandas DataFrame from ranking data"""
        if not rankings:
            return pd.DataFrame()

        ranking_data = []
        for rank, candidate in enumerate(rankings, 1):
            ranking_row = {
                'Rank': rank,
                'Name': candidate.get('candidate_name', 'N/A'),
                'Email': candidate.get('candidate_email', 'N/A'),
                'Match Score': candidate.get('match_score', 0),
                'Experience': candidate.get('experience_years', 0),
                'Strengths': ', '.join(candidate.get('strengths', [])),
                'Weaknesses': ', '.join(candidate.get('weaknesses', [])),
                'File Name': candidate.get('file_name', 'N/A')
            }
            ranking_data.append(ranking_row)
        return pd.DataFrame(ranking_data)

    # ---------------- Export ---------------- #
    def export_resumes_to_csv(self, resumes: List[Dict]) -> str:
        """Export parsed resumes to CSV string for download"""
        df = self.create_dataframe(resumes)
        if df.empty:
            return None
        return df.to_csv(index=False)

    def export_rankings_to_csv(self, rankings: List[Dict]) -> str:
        """Export rankings to CSV string for download"""
        df = self.create_ranking_dataframe(rankings)
        if df.empty:
            return None
        return df.to_csv(index=False)

    # ---------------- Stats ---------------- #
    def get_statistics(self, resumes: List[Dict]) -> Dict:
        """Get statistics about the parsed resumes"""
        if not resumes:
            return {}

        total_resumes = len(resumes)
        experience_years = [r.get('experience_years', 0) for r in resumes]
        avg_experience = sum(experience_years) / len(experience_years) if experience_years else 0

        all_skills = []
        for resume in resumes:
            all_skills.extend(resume.get('skills', []))

        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            'total_resumes': total_resumes,
            'average_experience': round(avg_experience, 1),
            'top_skills': top_skills,
            'experience_range': {
                'min': min(experience_years) if experience_years else 0,
                'max': max(experience_years) if experience_years else 0
            }
        }