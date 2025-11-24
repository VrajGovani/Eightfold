"""
PDF Service - Generates PDF reports
"""
import logging
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.models.report import PerformanceReport
from app.config import settings

logger = logging.getLogger(__name__)

class PDFService:
    """Generate PDF reports"""
    
    @staticmethod
    def generate_report_pdf(report: PerformanceReport) -> bytes:
        """Generate PDF from performance report"""
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        elements.append(Paragraph("Interview Performance Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Header info
        header_data = [
            ['Candidate:', report.candidate_name or 'N/A'],
            ['Role:', report.target_role],
            ['Date:', report.interview_date.strftime('%B %d, %Y')],
            ['Duration:', f"{report.duration_minutes:.1f} minutes"],
        ]
        
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Overall Score
        elements.append(Paragraph("Overall Performance", heading_style))
        
        score_color = PDFService._get_score_color(report.scores.overall)
        score_data = [
            ['Overall Score', f"{report.scores.overall}/100"],
            ['Recommendation', report.recommendation_level],
            ['Interview Ready', 'Yes' if report.ready_for_interviews else 'No'],
        ]
        
        score_table = Table(score_data, colWidths=[3*inch, 3*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Score Breakdown
        elements.append(Paragraph("Score Breakdown", heading_style))
        
        breakdown_data = [
            ['Metric', 'Score'],
            ['Confidence', f"{report.scores.confidence}/100"],
            ['Communication', f"{report.scores.communication}/100"],
            ['Technical Depth', f"{report.scores.technical_depth}/100"],
            ['STAR Method Usage', f"{report.scores.star_method_usage}/100"],
            ['Behavioral Clarity', f"{report.scores.behavioral_clarity}/100"],
        ]
        
        breakdown_table = Table(breakdown_data, colWidths=[3.5*inch, 2.5*inch])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(breakdown_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Strengths
        elements.append(Paragraph("Strengths", heading_style))
        for strength in report.overall_strengths[:5]:
            elements.append(Paragraph(f"• {strength}", styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
        elements.append(Spacer(1, 0.2*inch))
        
        # Areas for Improvement
        elements.append(Paragraph("Areas for Improvement", heading_style))
        for weakness in report.overall_weaknesses[:5]:
            elements.append(Paragraph(f"• {weakness}", styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
        elements.append(Spacer(1, 0.2*inch))
        
        # Improvement Suggestions
        elements.append(Paragraph("Improvement Suggestions", heading_style))
        for suggestion in report.improvement_suggestions[:7]:
            elements.append(Paragraph(f"• {suggestion}", styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
        elements.append(Spacer(1, 0.2*inch))
        
        # Next Steps
        elements.append(Paragraph("Recommended Next Steps", heading_style))
        for step in report.recommended_next_steps[:5]:
            elements.append(Paragraph(f"• {step}", styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
        
        # Build PDF
        doc.build(elements)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Generated PDF report for session {report.session_id}")
        return pdf_bytes
    
    @staticmethod
    def _get_score_color(score: float) -> colors.Color:
        """Get color based on score"""
        if score >= 75:
            return colors.HexColor('#28a745')  # Green
        elif score >= 60:
            return colors.HexColor('#ffc107')  # Yellow
        else:
            return colors.HexColor('#dc3545')  # Red
