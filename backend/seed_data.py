import json
from datetime import date

from sqlalchemy.orm import Session

from models import Opportunity

DEMO_OPPORTUNITIES = [
    {
        "title": "AI & Machine Learning Internship",
        "organization": "DemoTech Labs",
        "category": "Internship",
        "description": (
            "A hands-on internship focused on building and evaluating machine learning models for practical software applications."
        ),
        "required_skills": ["Python", "Machine Learning", "SQL"],
        "preferred_skills": ["TensorFlow", "Scikit-learn"],
        "eligibility": "B.Tech students in 2nd or 3rd year from CSE, IT, AI or related branches.",
        "location": "Remote",
        "deadline": date(2026, 10, 15),
        "application_url": "https://example.com/demo-ai-ml-internship",
    },
    {
        "title": "Data Science Internship",
        "organization": "DemoData Analytics",
        "category": "Internship",
        "description": (
            "Work on data analysis, visualization and predictive modeling using real-world style datasets."
        ),
        "required_skills": ["Python", "Pandas", "SQL"],
        "preferred_skills": ["Scikit-learn", "Data Visualization"],
        "eligibility": "Students pursuing undergraduate degrees in CSE, IT, Data Science or related fields.",
        "location": "Pune",
        "deadline": date(2026, 10, 20),
        "application_url": "https://example.com/demo-data-science-internship",
    },
    {
        "title": "Computer Vision Research Internship",
        "organization": "VisionForge Research",
        "category": "Internship",
        "description": (
            "Explore image classification and computer vision workflows through a research-oriented internship project."
        ),
        "required_skills": ["Python", "Computer Vision", "Deep Learning"],
        "preferred_skills": ["TensorFlow", "OpenCV"],
        "eligibility": "Open to 3rd and 4th year engineering students in AI, CSE or related branches.",
        "location": "Remote",
        "deadline": date(2026, 10, 25),
        "application_url": "https://example.com/demo-cv-research",
    },
    {
        "title": "Generative AI Hackathon",
        "organization": "FutureBuild Community",
        "category": "Hackathon",
        "description": (
            "Build an innovative application using generative AI, large language models or AI-powered automation."
        ),
        "required_skills": ["Python", "Generative AI"],
        "preferred_skills": ["LLMs", "FastAPI", "React"],
        "eligibility": "Open to undergraduate and postgraduate students. Teams of 2 to 4 members.",
        "location": "Remote",
        "deadline": date(2026, 11, 2),
        "application_url": "https://example.com/demo-genai-hackathon",
    },
    {
        "title": "Web Innovation Hackathon",
        "organization": "CodeSprint Demo",
        "category": "Hackathon",
        "description": (
            "Create a useful web application addressing a real-world problem using modern frontend technologies."
        ),
        "required_skills": ["HTML", "CSS", "JavaScript"],
        "preferred_skills": ["React", "Node.js"],
        "eligibility": "Open to all undergraduate students.",
        "location": "Pune",
        "deadline": date(2026, 11, 5),
        "application_url": "https://example.com/demo-web-hackathon",
    },
    {
        "title": "Open Source Contribution Challenge",
        "organization": "OpenCode Initiative",
        "category": "Competition",
        "description": (
            "Contribute to open-source projects and demonstrate practical software development and collaboration skills."
        ),
        "required_skills": ["Git", "GitHub"],
        "preferred_skills": ["Python", "JavaScript"],
        "eligibility": "Open to students with basic programming and version-control knowledge.",
        "location": "Remote",
        "deadline": date(2026, 11, 10),
        "application_url": "https://example.com/demo-open-source",
    },
    {
        "title": "Practical Machine Learning Workshop",
        "organization": "AI Learning Hub",
        "category": "Workshop",
        "description": (
            "A beginner-friendly workshop covering data preprocessing, model training and evaluation."
        ),
        "required_skills": ["Python"],
        "preferred_skills": ["Pandas", "Scikit-learn"],
        "eligibility": "Open to undergraduate students interested in machine learning.",
        "location": "Pune",
        "deadline": date(2026, 10, 8),
        "application_url": "https://example.com/demo-ml-workshop",
    },
    {
        "title": "Python Programming Certification",
        "organization": "SkillPath Academy",
        "category": "Certification",
        "description": (
            "A structured certification program covering Python programming, object-oriented programming and practical problem solving."
        ),
        "required_skills": ["Python"],
        "preferred_skills": ["Object-Oriented Programming"],
        "eligibility": "Open to students and recent graduates.",
        "location": "Online",
        "deadline": date(2026, 12, 1),
        "application_url": "https://example.com/demo-python-certification",
    },
    {
        "title": "Cloud Computing Fundamentals",
        "organization": "CloudStart Education",
        "category": "Certification",
        "description": (
            "Learn cloud fundamentals, containers, deployment concepts and basic cloud architecture."
        ),
        "required_skills": ["Programming"],
        "preferred_skills": ["Docker", "Cloud Computing"],
        "eligibility": "Open to undergraduate students from technical disciplines.",
        "location": "Online",
        "deadline": date(2026, 11, 20),
        "application_url": "https://example.com/demo-cloud-certification",
    },
    {
        "title": "AI Research Assistant Program",
        "organization": "FutureAI Research Center",
        "category": "Internship",
        "description": (
            "A research-focused student program covering machine learning, natural language processing and experimentation."
        ),
        "required_skills": ["Python", "Machine Learning"],
        "preferred_skills": ["NLP", "Deep Learning"],
        "eligibility": "Open to 3rd and 4th year students with an interest in AI research.",
        "location": "Remote",
        "deadline": date(2026, 10, 30),
        "application_url": "https://example.com/demo-ai-research",
    },
    {
        "title": "Women in Technology Scholarship",
        "organization": "FutureTech Foundation",
        "category": "Scholarship",
        "description": (
            "A demo scholarship program supporting students pursuing technology and computing education."
        ),
        "required_skills": [],
        "preferred_skills": ["Programming", "Technology"],
        "eligibility": "Open to eligible undergraduate students pursuing technology-related degrees.",
        "location": "India",
        "deadline": date(2026, 12, 10),
        "application_url": "https://example.com/demo-women-tech-scholarship",
    },
    {
        "title": "Startup Pitch Challenge",
        "organization": "CampusFounders Demo",
        "category": "Competition",
        "description": (
            "Present a technology-driven startup idea to a panel and receive feedback on product and business strategy."
        ),
        "required_skills": ["Problem Solving", "Presentation"],
        "preferred_skills": ["Entrepreneurship", "Technology"],
        "eligibility": "Open to undergraduate and postgraduate students.",
        "location": "Pune",
        "deadline": date(2026, 11, 15),
        "application_url": "https://example.com/demo-startup-pitch",
    },
    {
        "title": "Natural Language Processing Workshop",
        "organization": "LanguageAI Academy",
        "category": "Workshop",
        "description": (
            "Learn text preprocessing, classification, embeddings and modern NLP application development."
        ),
        "required_skills": ["Python", "NLP"],
        "preferred_skills": ["Machine Learning", "Transformers"],
        "eligibility": "Open to students with basic Python knowledge.",
        "location": "Online",
        "deadline": date(2026, 10, 18),
        "application_url": "https://example.com/demo-nlp-workshop",
    },
    {
        "title": "Data Analytics Career Course",
        "organization": "DataSkills Institute",
        "category": "Course",
        "description": (
            "Learn data cleaning, SQL analysis, dashboards and practical analytics workflows."
        ),
        "required_skills": ["SQL", "Excel"],
        "preferred_skills": ["Python", "Power BI"],
        "eligibility": "Open to undergraduate students and recent graduates.",
        "location": "Online",
        "deadline": date(2026, 11, 30),
        "application_url": "https://example.com/demo-data-course",
    },
    {
        "title": "Generative AI Bootcamp",
        "organization": "GenAI Learning Studio",
        "category": "Course",
        "description": (
            "An intensive learning program covering LLM fundamentals, prompt engineering, RAG and AI application development."
        ),
        "required_skills": ["Python"],
        "preferred_skills": ["LLMs", "LangChain", "APIs"],
        "eligibility": "Open to students with basic programming knowledge.",
        "location": "Online",
        "deadline": date(2026, 12, 5),
        "application_url": "https://example.com/demo-genai-bootcamp",
    },
    {
        "title": "Software Engineering Internship",
        "organization": "BuildStack Technologies",
        "category": "Internship",
        "description": (
            "Work with a development team on APIs, web applications, testing and software engineering practices."
        ),
        "required_skills": ["Python", "Git"],
        "preferred_skills": ["React", "FastAPI", "SQL"],
        "eligibility": "Open to 2nd and 3rd year students from CSE, IT or related branches.",
        "location": "Pune",
        "deadline": date(2026, 10, 28),
        "application_url": "https://example.com/demo-software-internship",
    },
    {
        "title": "Cybersecurity Fundamentals Workshop",
        "organization": "SecureCode Academy",
        "category": "Workshop",
        "description": (
            "Introduction to application security, common vulnerabilities, secure coding and cybersecurity fundamentals."
        ),
        "required_skills": ["Programming"],
        "preferred_skills": ["Networking", "Linux"],
        "eligibility": "Open to undergraduate students interested in cybersecurity.",
        "location": "Online",
        "deadline": date(2026, 11, 8),
        "application_url": "https://example.com/demo-cyber-workshop",
    },
    {
        "title": "Robotics and AI Competition",
        "organization": "RoboTech Campus",
        "category": "Competition",
        "description": (
            "Design an intelligent robotics solution combining programming, computer vision and machine learning."
        ),
        "required_skills": ["Python", "Programming"],
        "preferred_skills": ["Computer Vision", "Machine Learning"],
        "eligibility": "Open to engineering students. Teams of 2 to 5 members.",
        "location": "Pune",
        "deadline": date(2026, 11, 18),
        "application_url": "https://example.com/demo-robotics",
    },
    {
        "title": "Frontend Development Certification",
        "organization": "WebSkills Academy",
        "category": "Certification",
        "description": (
            "Build responsive web interfaces using HTML, CSS, JavaScript and modern frontend development practices."
        ),
        "required_skills": ["HTML", "CSS", "JavaScript"],
        "preferred_skills": ["React", "Git"],
        "eligibility": "Open to students interested in frontend development.",
        "location": "Online",
        "deadline": date(2026, 12, 15),
        "application_url": "https://example.com/demo-frontend-certification",
    },
    {
        "title": "AI Product Challenge",
        "organization": "ProductLabs Campus",
        "category": "Competition",
        "description": (
            "Design an AI-powered product concept and pitch a real-world use case to a panel of mentors and founders."
        ),
        "required_skills": ["Python", "Product Thinking", "Presentation"],
        "preferred_skills": ["AI", "Problem Solving", "Business Strategy"],
        "eligibility": "Open to undergraduate students with interest in AI products and entrepreneurship.",
        "location": "Remote",
        "deadline": date(2026, 12, 20),
        "application_url": "https://example.com/demo-ai-product-challenge",
    },
]


def seed_opportunities(db: Session):
    existing_count = db.query(Opportunity).count()

    if existing_count == len(DEMO_OPPORTUNITIES):
        return

    db.query(Opportunity).delete()

    opportunities = [
        Opportunity(
            title=opportunity_data["title"],
            organization=opportunity_data["organization"],
            category=opportunity_data["category"],
            description=opportunity_data["description"],
            required_skills=json.dumps(opportunity_data["required_skills"]),
            preferred_skills=json.dumps(opportunity_data["preferred_skills"]),
            eligibility=opportunity_data["eligibility"],
            location=opportunity_data["location"],
            deadline=opportunity_data["deadline"],
            application_url=opportunity_data["application_url"],
            is_demo=True,
        )
        for opportunity_data in DEMO_OPPORTUNITIES
    ]

    db.add_all(opportunities)
    db.commit()
