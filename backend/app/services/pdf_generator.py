"""
PDF Report Generator for ResumeAI
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.colors import HexColor
import io
from datetime import datetime
import os

class PDFGenerator:
    """Generate PDF reports for resume analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6C63FF'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2D3436'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#636E72'),
            spaceAfter=6,
            leading=16
        ))
        
        self.styles.add(ParagraphStyle(
            name='SkillTag',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#00B894'),
            backColor=colors.HexColor('#F0FFF4'),
            borderPadding=5,
            borderRadius=12,
            borderWidth=1,
            borderColor=colors.HexColor('#00B894')
        ))
    
    def generate_report(self, analysis_data, resume_data, job_data, output_path=None):
        """Generate a complete PDF report"""
        
        if output_path is None:
            output_path = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # ===== COVER PAGE =====
        story.extend(self._create_cover_page(analysis_data, resume_data, job_data))
        story.append(PageBreak())
        
        # ===== EXECUTIVE SUMMARY =====
        story.extend(self._create_executive_summary(analysis_data))
        story.append(PageBreak())
        
        # ===== SKILL ANALYSIS =====
        story.extend(self._create_skill_analysis(analysis_data))
        story.append(PageBreak())
        
        # ===== RECOMMENDATIONS =====
        story.extend(self._create_recommendations(analysis_data))
        story.append(PageBreak())
        
        # ===== DETAILED FINDINGS =====
        story.extend(self._create_detailed_findings(analysis_data, resume_data, job_data))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _create_cover_page(self, analysis_data, resume_data, job_data):
        """Create cover page"""
        story = []
        
        # Title
        story.append(Paragraph("Resume Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Date
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.5*inch))
        
        # Resume info
        story.append(Paragraph("Resume Information", self.styles['CustomHeading']))
        story.append(Paragraph(f"File: {resume_data.get('filename', 'Unknown')}", self.styles['CustomBody']))
        story.append(Paragraph(f"Skills: {', '.join(resume_data.get('skills', [])[:10])}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # Job info
        story.append(Paragraph("Job Information", self.styles['CustomHeading']))
        story.append(Paragraph(f"Title: {job_data.get('title', 'Unknown')}", self.styles['CustomBody']))
        story.append(Paragraph(f"Company: {job_data.get('company', 'Unknown')}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.5*inch))
        
        # Score
        score = analysis_data.get('overall_score', 0)
        story.append(Paragraph(f"Overall Compatibility Score: {score}%", self.styles['CustomHeading']))
        
        # Score bar
        story.append(self._create_score_bar(score))
        
        return story
    
    def _create_score_bar(self, score):
        """Create a visual score bar"""
        from reportlab.platypus import Table
        
        # Color based on score
        if score >= 70:
            color = '#00B894'
        elif score >= 40:
            color = '#FDCB6E'
        else:
            color = '#E17055'
        
        data = [
            ['', f'{score}%']
        ]
        
        table = Table(data, colWidths=[4*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#EDF2F7')),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor(color)),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 12),
            ('FONTSIZE', (1, 0), (1, 0), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return table
    
    def _create_executive_summary(self, analysis_data):
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        score = analysis_data.get('overall_score', 0)
        matching_count = len(analysis_data.get('matching_skills', []))
        missing_count = len(analysis_data.get('missing_skills', []))
        
        # Summary text
        if score >= 70:
            summary = "Your resume shows strong alignment with the job requirements."
        elif score >= 40:
            summary = "Your resume has moderate alignment with the job requirements."
        else:
            summary = "Your resume needs significant improvement to match this job."
        
        story.append(Paragraph(summary, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Key metrics
        metrics = [
            f"Compatibility Score: {score}%",
            f"Matching Skills: {matching_count}",
            f"Missing Skills: {missing_count}",
            f"Experience Match: {analysis_data.get('experience_match', 0)}%",
            f"Education Match: {analysis_data.get('education_match', 0)}%"
        ]
        
        for metric in metrics:
            story.append(Paragraph(f"• {metric}", self.styles['CustomBody']))
        
        return story
    
    def _create_skill_analysis(self, analysis_data):
        """Create skill analysis section"""
        story = []
        
        story.append(Paragraph("Skill Analysis", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        # Matching skills
        matching = analysis_data.get('matching_skills', [])
        if matching:
            story.append(Paragraph("✅ Matching Skills", self.styles['CustomHeading']))
            story.append(Paragraph(", ".join(matching[:15]), self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # Missing skills
        missing = analysis_data.get('missing_skills', [])
        if missing:
            story.append(Paragraph("❌ Missing Skills (Need to Learn)", self.styles['CustomHeading']))
            story.append(Paragraph(", ".join(missing[:15]), self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # Gap analysis
        gap_analysis = analysis_data.get('skill_gap_analysis', {})
        if gap_analysis:
            story.append(Paragraph("Skill Gap Summary", self.styles['CustomHeading']))
            categorized = gap_analysis.get('categorized_gaps', {})
            for category, skills in categorized.items():
                if skills:
                    story.append(Paragraph(f"{category.capitalize()}: {', '.join(skills)}", self.styles['CustomBody']))
        
        return story
    
    def _create_recommendations(self, analysis_data):
        """Create recommendations section"""
        story = []
        
        story.append(Paragraph("Learning Recommendations", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        recommendations = analysis_data.get('recommendations', {})
        
        # Learning path
        learning_path = recommendations.get('learning_path', [])
        if learning_path:
            story.append(Paragraph("📚 Learning Path", self.styles['CustomHeading']))
            for item in learning_path[:5]:
                story.append(Paragraph(
                    f"• {item.get('skill')} - {item.get('priority', 'medium')} priority, {item.get('estimated_time', '4-6 weeks')}",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 0.2*inch))
        
        # Courses
        courses = recommendations.get('courses', [])
        if courses:
            story.append(Paragraph("📖 Recommended Courses", self.styles['CustomHeading']))
            for course in courses[:5]:
                story.append(Paragraph(
                    f"• {course.get('name', 'Course')} ({course.get('platform', 'Online')})",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 0.2*inch))
        
        # Projects
        projects = recommendations.get('projects', [])
        if projects:
            story.append(Paragraph("🔨 Practice Projects", self.styles['CustomHeading']))
            for project in projects[:3]:
                story.append(Paragraph(
                    f"• {project.get('name', 'Project')}: {project.get('description', '')}",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 0.2*inch))
        
        # Certifications
        certifications = recommendations.get('certifications', [])
        if certifications:
            story.append(Paragraph("🎓 Recommended Certifications", self.styles['CustomHeading']))
            for cert in certifications[:3]:
                story.append(Paragraph(
                    f"• {cert.get('name', 'Certification')} ({cert.get('provider', '')})",
                    self.styles['CustomBody']
                ))
        
        # Tips
        tips = recommendations.get('tips', '')
        if tips:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("💡 Pro Tips", self.styles['CustomHeading']))
            story.append(Paragraph(tips, self.styles['CustomBody']))
        
        return story
    
    def _create_detailed_findings(self, analysis_data, resume_data, job_data):
        """Create detailed findings section"""
        story = []
        
        story.append(Paragraph("Detailed Findings", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        # Resume strengths
        story.append(Paragraph("Resume Strengths", self.styles['CustomHeading']))
        matching = analysis_data.get('matching_skills', [])
        if matching:
            story.append(Paragraph(f"• Strong match in: {', '.join(matching[:10])}", self.styles['CustomBody']))
        
        # Areas for improvement
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Areas for Improvement", self.styles['CustomHeading']))
        missing = analysis_data.get('missing_skills', [])
        if missing:
            story.append(Paragraph(f"• Learn: {', '.join(missing[:10])}", self.styles['CustomBody']))
        
        # Additional notes
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Notes", self.styles['CustomHeading']))
        story.append(Paragraph(
            "This analysis is based on the skills extracted from your resume and the job description. "
            "Focus on acquiring the missing skills to improve your compatibility score.",
            self.styles['CustomBody']
        ))
        
        return story
    
    def generate_bytes(self, analysis_data, resume_data, job_data):
        """Generate PDF and return as bytes"""
        output_path = self.generate_report(analysis_data, resume_data, job_data)
        with open(output_path, 'rb') as f:
            bytes_data = f.read()
        os.remove(output_path)  # Clean up
        return bytes_data

# Singleton instance
pdf_generator = PDFGenerator()

def get_pdf_generator():
    """Get PDF generator instance"""
    return pdf_generator