from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

OUT = "output/pdf/cenow_interview_handout.pdf"

navy = colors.HexColor("#101B46")
blue = colors.HexColor("#285C9B")
yellow = colors.HexColor("#F3C84B")
slate = colors.HexColor("#44546A")
light = colors.HexColor("#F2F6FA")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=navy, alignment=TA_CENTER, spaceAfter=7))
styles.add(ParagraphStyle(name="Sub", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=slate, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="H", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=navy, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=colors.HexColor("#1F2937"), spaceAfter=5))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.2, leading=11, textColor=colors.HexColor("#1F2937")))
styles.add(ParagraphStyle(name="Quote", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=9.4, leading=14, textColor=navy, leftIndent=12, rightIndent=12, spaceBefore=5, spaceAfter=9))

def p(text, style="BodyCustom"):
    return Paragraph(text, styles[style])

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(yellow)
    canvas.setLineWidth(1)
    canvas.line(doc.leftMargin, 0.47*inch, A4[0]-doc.rightMargin, 0.47*inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(slate)
    canvas.drawString(doc.leftMargin, 0.30*inch, "Cenow / B365 Advisors - Interview Preparation")
    canvas.drawRightString(A4[0]-doc.rightMargin, 0.30*inch, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=38, bottomMargin=48)
story = []
story += [p("Cenow / B365 Advisors", "TitleCustom"), p("Full-stack internship project - interview-ready architecture, contributions, and learning", "Sub")]

story += [p("Project summary", "H"), p("A full-stack corporate consulting website built to present services, capture business enquiries, accept job and internship applications, and let administrators manage career listings. The system combines a polished public website with email workflows, a jobs database, and an internal admin dashboard.")]

story += [p("System architecture", "H")]
arch_data = [
    [p("<b>Layer</b>", "Small"), p("<b>Responsibilities and technologies</b>", "Small")],
    [p("Client", "Small"), p("Responsive public pages, career flows, admin UI, animated components, and 3D office globe. Next.js 15, React 19, TypeScript, Tailwind CSS, Radix UI.", "Small")],
    [p("Interaction", "Small"), p("Framer Motion / GSAP animations; Three.js with React Three Fiber and Drei; Zustand state for globe view, rotation, selected locations, and information panel.", "Small")],
    [p("Application", "Small"), p("Next.js App Router pages, Route Handlers, and Server Actions. APIs process contact, partnership, job, and internship requests.", "Small")],
    [p("Data", "Small"), p("Prisma ORM connects the app to PostgreSQL. The Jobs model stores id, name, category, description, and link.", "Small")],
    [p("Communication", "Small"), p("Nodemailer and Gmail SMTP send internal notifications and automated acknowledgements. Job applications support resume and cover-letter attachments through FormData.", "Small")],
    [p("Supporting", "Small"), p("Vercel Analytics, Meta Pixel, Organization structured data, and chatbot embedding support measurement, discoverability, and engagement.", "Small")],
]
t = Table(arch_data, colWidths=[1.05*inch, 5.9*inch], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), navy), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("BACKGROUND", (0,1), (-1,-1), light), ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#C8D5E3")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
story += [t, Spacer(1, 8)]

story += [p("Request flow to explain in the interview", "H")]
flow = [[p("User", "Small"), p("Public page / form", "Small"), p("Next.js API or Server Action", "Small"), p("PostgreSQL or SMTP email", "Small")]]
ft = Table(flow, colWidths=[1.35*inch, 1.9*inch, 2.15*inch, 1.65*inch])
ft.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#EAF1F9")), ("GRID", (0,0), (-1,-1), 0.4, blue), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ALIGN", (0,0), (-1,-1), "CENTER"), ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6), ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)]))
story += [ft, Spacer(1, 8), p("Example: an applicant submits a job form with files; the browser sends FormData to the application route, the server converts attachments to buffers, Nodemailer sends the hiring notification and acknowledgement email, and the UI shows a success or failure state.")]

story += [PageBreak(), p("Separate contribution narratives", "H"), p("Use these role splits only when they truthfully reflect your work. Change ownership if your actual division was different.", "Quote")]

left = [p("Candidate 1 - Frontend and user experience", "H"), p("<b>Interview answer:</b>", "Small"), p("I primarily worked on the frontend and user experience. I built reusable React components and integrated them into Next.js App Router pages for the home, services, career, contact, and navigation experiences. I used Tailwind CSS to make layouts responsive for desktop and mobile users.", "Small"), p("I also worked on interactive elements such as animations with Framer Motion and GSAP, client-side form validation with loading and success states, and the interactive office-location globe. For the globe, I used React Three Fiber and Three.js, with Zustand to manage active locations, auto-rotation, display mode, and selected markers.", "Small"), p("<b>What I learned:</b> component-based development, TypeScript, responsive design, state management, animation, UI testing, API integration, and translating business requirements into usable interfaces.", "Small")]
right = [p("Candidate 2 - Backend and data workflows", "H"), p("<b>Interview answer:</b>", "Small"), p("My main contribution was backend integration and business workflows. I used Prisma ORM to connect the Next.js application to PostgreSQL and worked on the Jobs data model. I implemented the admin job-management flow so administrators can create, view, and delete job listings, with data reflected on the public career section.", "Small"), p("I also worked with Next.js Route Handlers for contact, partnership, job-application, and internship-application flows. These APIs process input, support multipart FormData and document attachments where needed, and use Nodemailer with environment variables to send internal alerts and automatic confirmations.", "Small"), p("<b>What I learned:</b> API design, Prisma and PostgreSQL, Server Actions, file handling, email workflows, error handling, environment-variable management, and backend security basics.", "Small")]
ct = Table([[left, right]], colWidths=[3.48*inch, 3.48*inch])
ct.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("BOX", (0,0), (0,0), 0.7, blue), ("BOX", (1,0), (1,0), 0.7, blue), ("BACKGROUND", (0,0), (-1,-1), colors.white), ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
story += [ct]

story += [p("Shared internship learning", "H"), p("We learned how a production-style web solution is delivered as a team: splitting work by modules, integrating frontend and backend changes, testing responsive behavior and form workflows, using Git for collaboration, and considering performance, usability, reliability, and security - not only visual design.")]

story += [p("30-second project introduction", "H"), p("During our internship, we developed a full-stack consulting-company website using Next.js, React, TypeScript, Tailwind CSS, Prisma, and PostgreSQL. The platform includes service pages, an interactive global-office globe, contact and partnership forms, job and internship applications with automated email confirmation, and an admin dashboard for job management. The project gave us practical experience in frontend-backend integration, database operations, API development, responsive design, and team delivery.", "Quote")]

story += [p("Likely interview questions", "H")]
qa = [
    [p("<b>Challenge?</b>", "Small"), p("Keeping career data dynamic while preserving a polished public UI. We separated responsibilities: admin management, Prisma persistence, API access, and public data display.", "Small")],
    [p("<b>Why Prisma?</b>", "Small"), p("It provides typed database access, a central schema, and simpler CRUD operations with PostgreSQL.", "Small")],
    [p("<b>Production improvement?</b>", "Small"), p("Replace prototype client-side admin state with server-side authentication, HTTP-only cookies, hashed passwords, role-based authorization, protected APIs, input/file validation, and rate limiting.", "Small")],
]
qt = Table(qa, colWidths=[1.4*inch, 5.55*inch])
qt.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), light), ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#C8D5E3")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
story += [qt]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
