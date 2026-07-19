import re
from typing import Dict, List, Any, Tuple

class ATSOptimizer:
    def __init__(self):
        self.ats_keywords = [
            'experienced', 'proficient', 'skilled', 'expert', 'professional',
            'certified', 'bachelor', 'master', 'degree', 'accomplished',
            'demonstrated', 'proven', 'strong', 'solid', 'extensive',
            'leadership', 'management', 'strategy', 'execution'
        ]
        
        self.bullet_patterns = [
            r'• [^\n]+',
            r'- [^\n]+',
            r'\d+\. [^\n]+'
        ]
    
    def analyze_ats_compatibility(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume's ATS compatibility"""
        issues = []
        suggestions = []
        
        # Check for keywords
        keyword_score = self._check_keywords(resume_text)
        
        # Check formatting
        format_score = self._check_formatting(resume_text)
        
        # Check for quantified achievements
        quant_score = self._check_quantified_achievements(resume_text)
        
        # Check for action verbs
        action_score = self._check_action_verbs(resume_text)
        
        total_score = (keyword_score + format_score + quant_score + action_score) / 4
        
        # Generate suggestions
        if keyword_score < 70:
            suggestions.append("Add more industry-specific keywords from job descriptions")
            issues.append("Limited keyword density")
        
        if format_score < 60:
            suggestions.append("Use standard formatting with clear headings and bullet points")
            issues.append("Poor formatting for ATS parsing")
        
        if quant_score < 50:
            suggestions.append("Include quantified achievements (e.g., 'increased sales by 20%')")
            issues.append("Lack of quantifiable results")
        
        if action_score < 60:
            suggestions.append("Start bullet points with strong action verbs")
            issues.append("Weak action verbs used")
        
        return {
            'total_score': total_score,
            'keyword_score': keyword_score,
            'format_score': format_score,
            'quant_score': quant_score,
            'action_score': action_score,
            'issues': issues,
            'suggestions': suggestions
        }
    
    def _check_keywords(self, text: str) -> float:
        """Check for ATS keywords in resume"""
        text_lower = text.lower()
        found_keywords = 0
        
        for keyword in self.ats_keywords:
            if keyword.lower() in text_lower:
                found_keywords += 1
        
        return (found_keywords / len(self.ats_keywords)) * 100
    
    def _check_formatting(self, text: str) -> float:
        """Check formatting for ATS compatibility"""
        score = 100
        
        # Check for proper bullet points
        has_bullets = False
        for pattern in self.bullet_patterns:
            if re.search(pattern, text):
                has_bullets = True
                break
        
        if not has_bullets:
            score -= 30
        
        # Check for clear section headers
        section_headers = ['experience', 'education', 'skills', 'summary']
        has_headers = 0
        for header in section_headers:
            if re.search(r'\b' + header + r'\b', text, re.IGNORECASE):
                has_headers += 1
        
        if has_headers < 2:
            score -= 20
        
        return max(0, score)
    
    def _check_quantified_achievements(self, text: str) -> float:
        """Check for quantified achievements"""
        # Look for percentages, numbers, and dollar amounts
        patterns = [
            r'\d+%',
            r'\d+\s*(?:percent|%)',
            r'\$\s?\d+[,.]?\d*',
            r'increased|decreased|reduced|improved|boosted',
            r'by\s+\d+%'
        ]
        
        found = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found += 1
        
        # Cap at 100
        return min(100, found * 20)
    
    def _check_action_verbs(self, text: str) -> float:
        """Check for strong action verbs"""
        action_verbs = [
            'achieved', 'improved', 'implemented', 'managed', 'developed',
            'created', 'designed', 'led', 'spearheaded', 'initiated',
            'optimized', 'streamlined', 'transformed', 'enhanced', 'established',
            'delivered', 'solved', 'built', 'coordinated', 'advised'
        ]
        
        found_verbs = 0
        text_lower = text.lower()
        
        for verb in action_verbs:
            if verb in text_lower:
                found_verbs += 1
        
        return min(100, (found_verbs / 10) * 100)
    
    def generate_ats_optimizations(self, resume_text: str) -> Dict[str, List[str]]:
        """Generate specific ATS optimizations"""
        suggestions = []
        keyword_suggestions = []
        
        # Keyword suggestions based on analysis
        for keyword in self.ats_keywords:
            if keyword not in resume_text.lower():
                keyword_suggestions.append(f"Add '{keyword}' to your resume")
        
        # Formatting suggestions
        if not re.search(r'\bexperience\b', resume_text, re.IGNORECASE):
            suggestions.append("Add a clear 'Experience' section header")
        
        if not re.search(r'\bskills\b', resume_text, re.IGNORECASE):
            suggestions.append("Add a clear 'Skills' section with relevant technologies")
        
        if not re.search(r'\b(?:summary|objective|profile)\b', resume_text, re.IGNORECASE):
            suggestions.append("Add a professional summary at the top")
        
        return {
            'keyword_suggestions': keyword_suggestions[:10],
            'formatting_suggestions': suggestions,
            'general_suggestions': [
                "Use consistent formatting throughout",
                "Keep resume to 1-2 pages",
                "Use standard fonts (Arial, Calibri, Times New Roman)",
                "Avoid tables and graphics",
                "Save as PDF or DOCX format"
            ]
        }