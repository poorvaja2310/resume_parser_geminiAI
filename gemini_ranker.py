# """
# Gemini AI integration for resume ranking and job matching
# """

# import google.generativeai as genai
# import json
# import os
# from typing import List, Dict
# import re

# class GeminiRanker:
#     def __init__(self, api_key: str):
#         """Initialize Gemini AI client"""
#         genai.configure(api_key=api_key)
#         self.model = genai.GenerativeModel('gemini-pro')
    
#     def create_ranking_prompt(self, job_description: str, resume_data: Dict) -> str:
#         """Create a prompt for ranking a resume against a job description"""
        
#         prompt = f"""
# You are an expert HR recruiter tasked with evaluating how well a candidate matches a job description.

# JOB DESCRIPTION:
# {job_description}

# CANDIDATE PROFILE:
# - Name: {resume_data.get('name', 'N/A')}
# - Email: {resume_data.get('email', 'N/A')}
# - Experience: {resume_data.get('experience_years', 0)} years
# - Skills: {', '.join(resume_data.get('skills', []))}
# - Education: {', '.join(resume_data.get('education', []))}
# - Raw Resume Text (excerpt): {resume_data.get('raw_text', '')[:500]}...

# EVALUATION CRITERIA:
# 1. Skills Match (40%): How well do the candidate's skills align with job requirements?
# 2. Experience Match (30%): Does the experience level and type match the position?
# 3. Education Match (20%): Is the educational background relevant?
# 4. Overall Fit (10%): General suitability based on the resume content.

# Please provide:
# 1. A match score from 0-100 (where 100 is perfect match)
# 2. A brief explanation (2-3 sentences) of why this score was given
# 3. Top 3 strengths of this candidate for this role
# 4. Top 2 areas where the candidate might not be ideal

# Format your response as JSON:
# {{
#     "match_score": [score 0-100],
#     "explanation": "[brief explanation]",
#     "strengths": ["strength 1", "strength 2", "strength 3"],
#     "weaknesses": ["weakness 1", "weakness 2"]
# }}
# """
#         return prompt
    
#     def rank_candidate(self, job_description: str, resume_data: Dict) -> Dict:
#         """Rank a single candidate against a job description"""
#         try:
#             prompt = self.create_ranking_prompt(job_description, resume_data)
#             response = self.model.generate_content(prompt)
            
#             # Extract JSON from response
#             response_text = response.text
            
#             # Try to find JSON in the response
#             json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
#             if json_match:
#                 json_str = json_match.group()
#                 ranking_data = json.loads(json_str)
                
#                 # Add candidate info to ranking
#                 ranking_data.update({
#                     'candidate_name': resume_data.get('name', 'N/A'),
#                     'candidate_email': resume_data.get('email', 'N/A'),
#                     'experience_years': resume_data.get('experience_years', 0),
#                     'file_name': resume_data.get('file_name', 'N/A')
#                 })
                
#                 return ranking_data
#             else:
#                 # Fallback if JSON parsing fails
#                 return {
#                     'match_score': 50,
#                     'explanation': 'Unable to parse AI response properly',
#                     'strengths': ['Resume processed'],
#                     'weaknesses': ['Analysis incomplete'],
#                     'candidate_name': resume_data.get('name', 'N/A'),
#                     'candidate_email': resume_data.get('email', 'N/A'),
#                     'experience_years': resume_data.get('experience_years', 0),
#                     'file_name': resume_data.get('file_name', 'N/A')
#                 }
                
#         except Exception as e:
#             print(f"Error ranking candidate: {e}")
#             return {
#                 'match_score': 0,
#                 'explanation': f'Error during evaluation: {str(e)}',
#                 'strengths': [],
#                 'weaknesses': ['Evaluation failed'],
#                 'candidate_name': resume_data.get('name', 'N/A'),
#                 'candidate_email': resume_data.get('email', 'N/A'),
#                 'experience_years': resume_data.get('experience_years', 0),
#                 'file_name': resume_data.get('file_name', 'N/A')
#             }
    
#     def rank_all_candidates(self, job_description: str, resumes_data: List[Dict]) -> List[Dict]:
#         """Rank all candidates against a job description"""
#         rankings = []
        
#         for resume_data in resumes_data:
#             ranking = self.rank_candidate(job_description, resume_data)
#             rankings.append(ranking)
        
#         # Sort by match score (highest first)
#         rankings.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
#         return rankings
    
#     def generate_summary_report(self, rankings: List[Dict], job_description: str) -> str:
#         """Generate a summary report of all rankings"""
#         if not rankings:
#             return "No candidates were evaluated."
        
#         top_candidates = rankings[:5]  # Top 5 candidates
#         avg_score = sum(r.get('match_score', 0) for r in rankings) / len(rankings)
        
#         summary_prompt = f"""
# Based on the evaluation of {len(rankings)} candidates for the following job description:

# JOB DESCRIPTION: {job_description[:500]}...

# TOP 5 CANDIDATES:
# {json.dumps(top_candidates, indent=2)}

# OVERALL STATS:
# - Total candidates evaluated: {len(rankings)}
# - Average match score: {avg_score:.1f}
# - Highest score: {rankings[0].get('match_score', 0)}
# - Lowest score: {rankings[-1].get('match_score', 0)}

# Please provide a brief executive summary (3-4 sentences) highlighting:
# 1. The overall quality of the candidate pool
# 2. Key trends in strengths/weaknesses
# 3. Recommendations for next steps

# Keep the response concise and professional.
# """
        
#         try:
#             response = self.model.generate_content(summary_prompt)
#             return response.text
#         except Exception as e:
#             return f"Unable to generate summary report: {str(e)}"
"""
Gemini AI integration for resume ranking and job matching
"""

import google.generativeai as genai
import json
import re
from typing import List, Dict


class GeminiRanker:
    def __init__(self, api_key: str):
        """Initialize Gemini AI client"""
        genai.configure(api_key=api_key)
        # Use free, fast Gemini model
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def create_ranking_prompt(self, job_description: str, resume_data: Dict) -> str:
        """Create a prompt for ranking a resume against a job description"""

        prompt = f"""
You are an expert HR recruiter tasked with evaluating how well a candidate matches a job description.

JOB DESCRIPTION:
{job_description}

CANDIDATE PROFILE:
- Name: {resume_data.get('name', 'N/A')}
- Email: {resume_data.get('email', 'N/A')}
- Experience: {resume_data.get('experience_years', 0)} years
- Skills: {', '.join(resume_data.get('skills', []))}
- Education: {', '.join(resume_data.get('education', []))}
- Summary: {resume_data.get('summary', 'No summary available')}

EVALUATION CRITERIA:
1. Skills Match (40%): How well do the candidate's skills align with job requirements?
2. Experience Match (30%): Does the experience level and type match the position?
3. Education Match (20%): Is the educational background relevant?
4. Overall Fit (10%): General suitability based on the resume content.

Please provide:
1. A match score from 0-100 (where 100 is perfect match)
2. A brief explanation (2-3 sentences) of why this score was given
3. Top 3 strengths of this candidate for this role
4. Top 2 areas where the candidate might not be ideal

Format your response strictly as JSON:
{{
    "match_score": [score 0-100],
    "explanation": "[brief explanation]",
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "weaknesses": ["weakness 1", "weakness 2"]
}}
"""
        return prompt

    def extract_json(self, response_text: str) -> Dict:
        """Extract JSON object from AI response"""
        try:
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        return None

    def rank_candidate(self, job_description: str, resume_data: Dict) -> Dict:
        """Rank a single candidate against a job description"""
        try:
            prompt = self.create_ranking_prompt(job_description, resume_data)
            response = self.model.generate_content(prompt)

            response_text = response.text.strip()
            ranking_data = self.extract_json(response_text)

            if ranking_data:
                ranking_data.update({
                    "candidate_name": resume_data.get("name", "N/A"),
                    "candidate_email": resume_data.get("email", "N/A"),
                    "experience_years": resume_data.get("experience_years", 0),
                    "file_name": resume_data.get("file_name", "N/A")
                })
                return ranking_data
            else:
                return {
                    "match_score": 50,
                    "explanation": "AI response could not be parsed properly.",
                    "strengths": ["Resume processed"],
                    "weaknesses": ["Analysis incomplete"],
                    "candidate_name": resume_data.get("name", "N/A"),
                    "candidate_email": resume_data.get("email", "N/A"),
                    "experience_years": resume_data.get("experience_years", 0),
                    "file_name": resume_data.get("file_name", "N/A"),
                }

        except Exception as e:
            return {
                "match_score": 0,
                "explanation": f"Error during evaluation: {str(e)}",
                "strengths": [],
                "weaknesses": ["Evaluation failed"],
                "candidate_name": resume_data.get("name", "N/A"),
                "candidate_email": resume_data.get("email", "N/A"),
                "experience_years": resume_data.get("experience_years", 0),
                "file_name": resume_data.get("file_name", "N/A"),
            }

    def rank_all_candidates(self, job_description: str, resumes_data: List[Dict]) -> List[Dict]:
        """Rank all candidates against a job description"""
        rankings = [self.rank_candidate(job_description, r) for r in resumes_data]
        rankings.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return rankings

    def generate_summary_report(self, rankings: List[Dict], job_description: str) -> str:
        """Generate a summary report of all rankings"""
        if not rankings:
            return "No candidates were evaluated."

        top_candidates = rankings[:5]  # Top 5 candidates
        avg_score = sum(r.get("match_score", 0) for r in rankings) / len(rankings)

        summary_prompt = f"""
Based on the evaluation of {len(rankings)} candidates for the following job description:

JOB DESCRIPTION (truncated): {job_description[:500]}...

TOP 5 CANDIDATES:
{json.dumps(top_candidates, indent=2)}

OVERALL STATS:
- Total candidates evaluated: {len(rankings)}
- Average match score: {avg_score:.1f}
- Highest score: {rankings[0].get("match_score", 0)}
- Lowest score: {rankings[-1].get("match_score", 0)}

Please provide a brief executive summary (3-4 sentences) highlighting:
1. The overall quality of the candidate pool
2. Key trends in strengths/weaknesses
3. Recommendations for next steps

Keep the response concise and professional.
"""

        try:
            response = self.model.generate_content(summary_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Unable to generate summary report: {str(e)}"