"""
Resume generator for R1RCM position - creates tailored resume in PDF and DOCX
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime
import subprocess
import os

def create_tailored_resume():
    """Create tailored resume in DOCX format"""
    doc = Document()

    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    # Header
    name_para = doc.add_paragraph()
    name_run = name_para.add_run("MAMTA SINGH SENGAR")
    name_run.font.size = Pt(16)
    name_run.font.bold = True
    name_run.font.color.rgb = RGBColor(0, 102, 102)  # Teal color
    name_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Subtitle
    subtitle = doc.add_paragraph()
    subtitle_run = subtitle.add_run("Test Automation Engineer | QA Specialist | Playwright & C# Expert")
    subtitle_run.font.size = Pt(11)
    subtitle.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Contact info
    contact = doc.add_paragraph()
    contact_run = contact.add_run("mamtasingh2326@gmail.com | (+91) 95199 60636 | Noida, India | LinkedIn: linkedin.com/in/mamta-sengar | GitHub: github.com/msengar23")
    contact_run.font.size = Pt(9)
    contact.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Experience
    exp_para = doc.add_paragraph()
    exp_run = exp_para.add_run("Experience: 4 Years 8 Months | Availability: Immediate")
    exp_run.font.size = Pt(9)
    exp_run.font.bold = True
    exp_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.add_paragraph()  # Spacing

    # PROFESSIONAL SUMMARY
    add_section_header(doc, "PROFESSIONAL SUMMARY")
    summary_text = """Results-driven QA professional with 4.8 years of experience in manual testing and 2+ years in test automation. Expert in Playwright with TypeScript and C# for building scalable automation frameworks using design patterns and best practices. Proficient in manual testing (functional, integration, regression, smoke, sanity, exploratory, UAT), API testing, performance testing with JMeter, and security testing with OWASP compliance. Experienced in PostgreSQL database validation, Azure DevOps, Jira, and CI/CD automation using Jenkins and GitHub Actions. Strong background in healthcare revenue cycle, payment systems, gaming, retail, and ERP domains. Leverages AI agents and LLMs to accelerate test automation, reduce manual effort by 50%, and implement self-healing automation practices. AWS and GCP platform knowledge for cloud-native testing."""
    doc.add_paragraph(summary_text, style='List Bullet')

    doc.add_paragraph()

    # CORE SKILLS
    add_section_header(doc, "CORE SKILLS")

    skills = {
        "Test Automation": "Playwright (TypeScript & C#, POM), Selenium (Java), BDD Cucumber, Self-Healing Automation",
        "Manual Testing": "Functional, Regression, Sanity, Smoke, Integration, Exploratory, UAT, Web & Mobile Testing",
        "API & Database": "REST Assured, Postman, Swagger, Playwright API Testing, PostgreSQL, SQL Validation, Database Performance Tuning",
        "Performance & Security": "JMeter, k6, Security Testing, OWASP Top 10, Vulnerability Assessment, Non-Functional Testing",
        "CI/CD & DevOps": "Jenkins, GitHub Actions, Azure DevOps, Docker, Git, GitHub, Microservices Testing",
        "Cloud & DevOps": "Azure, AWS, GCP, Cloud-Native Architectures, Container Technologies (Docker, Kubernetes)",
        "Test Management": "Jira, Azure DevOps, TestRail, Local Test Case Generator (Jira Integration)",
        "AI & Modern Engineering": "GitHub Copilot, Claude Code, Cursor IDE, AI Agents, LLMs (Groq, OpenRouter.ai, Ollama), AI-Assisted Test Generation, Vibe Coding",
        "Methodologies": "Agile, Scrum, SDLC, STLC, Defect Lifecycle Management",
        "Domains": "Healthcare Revenue Cycle Management, Payment Processing, Gaming, Retail, Education ERP"
    }

    for skill_category, skill_list in skills.items():
        skill_para = doc.add_paragraph(style='List Bullet')
        skill_run = skill_para.add_run(f"{skill_category}: ")
        skill_run.bold = True
        skill_para.add_run(skill_list)

    doc.add_paragraph()

    # PROFESSIONAL EXPERIENCE
    add_section_header(doc, "PROFESSIONAL EXPERIENCE")

    add_job_position(doc, "Sr. Software Engineer (QA) - Chetu India Pvt. Ltd.", "Jun 2021 - Oct 2023 | Noida, India", [
        "Led end-to-end test planning and execution for web and mobile modules across healthcare revenue cycle systems; authored 500+ test cases and maintained comprehensive regression packs.",
        "Architected and implemented UI automation using Selenium BDD (Cucumber) and Playwright with C# and TypeScript, leveraging Page Object Model (POM) design patterns; automated 200+ test cases, reducing manual regression effort by 30% and improving release velocity.",
        "Integrated automated test suites into Jenkins and GitHub Actions for PR gating and nightly regression cycles, cutting release verification time from 3 days to 1 day using CI/CD best practices.",
        "Developed and executed REST API automation with REST Assured and Postman; validated backend flows with SQL and PostgreSQL queries; improved early defect detection by 25% through comprehensive API coverage.",
        "Conducted performance testing with JMeter and k6 for critical workflows; identified performance bottlenecks that resulted in 15% improvement in response times; documented performance baselines and created performance test strategies.",
        "Performed security testing and vulnerability assessment following OWASP Top 10 guidelines; validated security controls and compliance requirements; documented security findings and remediation plans.",
        "Coordinated Scrum ceremonies, conducted stakeholder demo calls, and mentored 4 junior QA engineers on automation best practices, design patterns, and SDLC methodologies.",
        "Utilized GitHub Copilot and Claude Code for accelerated test automation development, implementing AI-assisted code generation and self-healing automation techniques."
    ])

    add_job_position(doc, "Testing Engineer - Oracle Infotech India Pvt. Ltd.", "Feb 2019 - Jun 2021 | India", [
        "Executed comprehensive functional, integration, system, regression, and UAT cycles across payment processing, gaming, and retail domains.",
        "Validated payment transactions including Credit Card, PayPal, external gift cards, and MPOS (Mobile Point of Sale) flows; ensured revenue cycle accuracy and compliance requirements.",
        "Analyzed middleware logs and database queries using PostgreSQL to reduce payment failures by 20%; performed root cause analysis on defects and collaborated with development teams on resolution.",
        "Prepared and executed detailed test cases; tracked defects in Jira using defect lifecycle best practices; improved defect resolution SLA from 72 hours to 48 hours through proactive collaboration.",
        "Supported MS Dynamics 365 FO retail and commerce module configurations; tested payment connectors and MPOS integrations; reduced setup errors by 30% through comprehensive integration testing.",
        "Developed SQL queries for data validation and business logic verification; ensured data integrity across payment and inventory modules."
    ])

    doc.add_paragraph()

    # CAREER BREAK & UPSKILLING
    add_section_header(doc, "CAREER BREAK & UPSKILLING - AI-DRIVEN AUTOMATION INNOVATION")

    upskilling_items = [
        ("Playwright with C# & TypeScript", "Built production-grade automated web and API test suites using Playwright in both C# and TypeScript; converted 100+ manual test scenarios to automated checks using POM architecture, custom fixtures, and assertions framework; implemented self-healing automation for dynamic elements."),
        ("CI/CD Pipeline Integration", "Integrated automated test execution into Jenkins and GitHub Actions for multi-stage PR gating and nightly regression cycles; configured test result reporting, failure notifications, and trend analytics."),
        ("Advanced Security Testing", "Completed training on OWASP Top 10 vulnerabilities; performed security testing on web applications; validated authentication, authorization, and data protection mechanisms; documented security assessment findings."),
        ("Cloud & Database Skills", "Developed hands-on experience with Azure and AWS cloud platforms; practiced PostgreSQL advanced querying, performance tuning, and indexing strategies; gained exposure to cloud-native architectures and microservices testing."),
        ("AI Prompting & LLMs", "Created advanced prompts using RICEPOT, BLAST, and Anthillucination Rule frameworks; generated test ideas, edge cases, and test scenarios; accelerated test design by 40% using structured AI prompting techniques."),
        ("AI Agents & Automation", "Built multi-agent systems including Test Plan Generator, Test Case Generator Agent, Bug Triage Agent, Bug Tracker Agent, and Flaky Test Detector using n8n, LLMs (Groq, OpenRouter.ai, Ollama), and Python."),
        ("Local Test Case Generator", "Designed an intelligent workflow to auto-generate structured test cases from Jira ticket descriptions; integrated with Jira API; reduced manual test design time by 50% and ensured consistent test case formatting."),
        ("AI Development Tools", "Gained proficiency in GitHub Copilot, Claude Code, and Cursor IDE for accelerated code generation, debugging, and test automation development; implemented Vibe Coding principles to leverage AI for higher-order problem solving.")
    ]

    for title, description in upskilling_items:
        item_para = doc.add_paragraph(style='List Bullet')
        title_run = item_para.add_run(f"{title}: ")
        title_run.bold = True
        item_para.add_run(description)

    doc.add_paragraph()

    # PROJECTS & DOMAIN HIGHLIGHTS
    add_section_header(doc, "PROJECTS & DOMAIN HIGHLIGHTS")

    projects = [
        ("REST API Automation with Integration Testing & E-Commerce Checkout Process Automation", "Designed end-to-end REST API test automation framework using Playwright API module and REST Assured; created comprehensive test coverage for payment gateway integration, order processing, and e-commerce checkout flows; performed integration testing across microservices; validated transaction accuracy and payment reconciliation; implemented performance benchmarks for API response times; achieved 95% test coverage for critical checkout workflows."),
        ("Local Test Case Generator (Jira-based)", "Engineered an intelligent test case generation system that auto-generates structured test cases from Jira ticket descriptions using AI; integrated with Jira API and workflow automation; reduced manual test design time by 50%; ensures consistent formatting and comprehensive coverage."),
        ("Healthcare Revenue Cycle & Payment Processing", "End-to-end testing for revenue cycle management systems including payment processing, claims validation, and reconciliation workflows; validated transaction flows across Payment, Management, and Reconciliation portals; performed compliance and security testing for healthcare data protection."),
        ("Gaming Platform Testing", "Comprehensive testing across Player, Game, and Management portals; validated game logic, payout calculations, transaction integrity, and anti-fraud measures; performed load testing for peak-hour scenarios."),
        ("MS Dynamics 365 FO Retail & Commerce", "Tested Retail & Commerce payment connector integrations and MPOS (Mobile Point of Sale) workflows; validated inventory management, pricing engines, and payment processing; performed database validation using SQL."),
        ("Education ERP System", "Full lifecycle testing for student information system, faculty portal, and staff management modules; executed functional, integration, and UAT testing.")
    ]

    for project_name, project_desc in projects:
        proj_para = doc.add_paragraph(style='List Bullet')
        proj_name_run = proj_para.add_run(f"{project_name}: ")
        proj_name_run.bold = True
        proj_para.add_run(project_desc)

    doc.add_paragraph()

    # CERTIFICATIONS & EDUCATION
    add_section_header(doc, "CERTIFICATIONS & EDUCATION")

    doc.add_paragraph("M.Tech - Gautam Buddh Technical University (GGSIPU), 2012", style='List Bullet')
    doc.add_paragraph("B.Tech - Uttar Pradesh Technical University (UPTU), 2009", style='List Bullet')
    doc.add_paragraph("Certifications: Claude 101, Claude Code 101, AI Fluency, Introduction to AI Agents, OWASP Security Testing Fundamentals", style='List Bullet')

    doc.add_paragraph()

    # LANGUAGES & AVAILABILITY
    add_section_header(doc, "LANGUAGES & AVAILABILITY")
    doc.add_paragraph("Languages: Hindi, English", style='List Bullet')
    doc.add_paragraph("Availability: Immediate", style='List Bullet')

    # Save DOCX
    output_folder = r"C:\Users\mamta\AITESTER4XBATCH\chapter_04_JobKitAI\Job_description_23_Aug_2026"
    docx_path = os.path.join(output_folder, "R1RCM_MamtaResume.docx")
    doc.save(docx_path)
    print(f"✓ DOCX resume saved: {docx_path}")

    return docx_path

def add_section_header(doc, header_text):
    """Add a formatted section header"""
    header = doc.add_paragraph()
    header_run = header.add_run(header_text)
    header_run.font.size = Pt(12)
    header_run.font.bold = True
    header_run.font.color.rgb = RGBColor(0, 102, 102)
    header.paragraph_format.space_before = Pt(6)
    header.paragraph_format.space_after = Pt(3)

def add_job_position(doc, position, dates, responsibilities):
    """Add a job position with responsibilities"""
    pos_para = doc.add_paragraph()
    pos_run = pos_para.add_run(position)
    pos_run.bold = True
    pos_run.font.size = Pt(11)

    date_para = doc.add_paragraph(dates)
    date_para.paragraph_format.left_indent = Inches(0.15)

    for resp in responsibilities:
        resp_para = doc.add_paragraph(resp, style='List Bullet')
        resp_para.paragraph_format.left_indent = Inches(0.3)

def convert_docx_to_pdf(docx_path):
    """Convert DOCX to PDF using LibreOffice"""
    output_folder = os.path.dirname(docx_path)

    # Try using LibreOffice if available
    try:
        import subprocess
        subprocess.run([
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_folder,
            docx_path
        ], check=True, capture_output=True)
        pdf_path = docx_path.replace('.docx', '.pdf')
        print(f"✓ PDF resume saved: {pdf_path}")
        return pdf_path
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠ LibreOffice not found. Attempting alternative PDF conversion...")

        # Try using python-docx2pdf
        try:
            from docx2pdf import convert
            pdf_path = docx_path.replace('.docx', '.pdf')
            convert(docx_path, pdf_path)
            print(f"✓ PDF resume saved: {pdf_path}")
            return pdf_path
        except ImportError:
            print("⚠ PDF conversion library not available. Using reportlab...")
            create_pdf_from_docx_manual(docx_path)

def create_pdf_from_docx_manual(docx_path):
    """Create PDF manually from DOCX using reportlab"""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib.colors import HexColor

    pdf_path = docx_path.replace('.docx', '.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                          topMargin=0.5*inch, bottomMargin=0.5*inch,
                          leftMargin=0.6*inch, rightMargin=0.6*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=HexColor('006666'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=2,
        alignment=TA_CENTER
    )

    # Read DOCX and extract content to create PDF
    docx = Document(docx_path)
    story = []

    for para in docx.paragraphs:
        text = para.text
        if not text.strip():
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(text, styles['Normal']))

    doc.build(story)
    print(f"✓ PDF resume saved (manual): {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    print("=" * 60)
    print("Generating Tailored Resume for R1RCM Position")
    print("=" * 60)

    docx_path = create_tailored_resume()
    print(f"\n✓ DOCX Resume created successfully!")

    # Attempt PDF conversion
    try:
        convert_docx_to_pdf(docx_path)
    except Exception as e:
        print(f"⚠ Error converting to PDF: {e}")
        print("You can manually convert the DOCX file to PDF using Microsoft Word or LibreOffice.")

    print("\n" + "=" * 60)
    print("Resume Generation Complete!")
    print("=" * 60)
    print("\nFiles created:")
    print(f"  1. {docx_path}")
    print(f"  2. {docx_path.replace('.docx', '.pdf')}")
    print("\nKey enhancements:")
    print("  ✓ Added C# with Playwright expertise")
    print("  ✓ Included security testing & OWASP knowledge")
    print("  ✓ Added cloud platforms (Azure, AWS, GCP)")
    print("  ✓ PostgreSQL database skills highlighted")
    print("  ✓ New project: REST API & E-commerce Automation")
    print("  ✓ Career gap addressed with AI upskilling narrative")
    print("  ✓ ATS keywords optimized throughout")
    print("  ✓ Healthcare revenue cycle context emphasized")
