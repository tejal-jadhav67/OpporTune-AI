import re

try:
    from .models import Opportunity, Student
except ImportError:  # pragma: no cover
    from models import Opportunity, Student

SKILL_WEIGHT = 40
INTEREST_WEIGHT = 20
ELIGIBILITY_WEIGHT = 20
LOCATION_WEIGHT = 10
CATEGORY_WEIGHT = 10

SKILL_ALIASES = {
    "ml": "machine learning",
    "machinelearning": "machine learning",
    "ai": "artificial intelligence",
    "artificialintelligence": "artificial intelligence",
    "dl": "deep learning",
    "deeplearning": "deep learning",
    "nlp": "natural language processing",
    "naturallanguageprocessing": "natural language processing",
    "cv": "computer vision",
    "computervision": "computer vision",
    "genai": "generative ai",
    "generativeai": "generative ai",
    "llm": "large language models",
    "llms": "large language models",
    "large language model": "large language models",
    "large language models": "large language models",
    "scikitlearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tf": "tensorflow",
    "js": "javascript",
    "reactjs": "react",
    "postgres": "postgresql",
    "c plus plus": "cpp",
    "c++": "cpp",
}

INTEREST_GROUPS = {
    "ai": {
        "artificial intelligence",
        "ai",
        "machine learning",
        "ml",
        "deep learning",
        "computer vision",
        "natural language processing",
        "nlp",
        "generative ai",
        "large language models",
        "llm",
        "robotics",
    },
    "data": {
        "data science",
        "data analytics",
        "analytics",
        "data engineering",
        "statistics",
        "business intelligence",
    },
    "web": {
        "web development",
        "frontend development",
        "backend development",
        "full stack development",
        "frontend",
        "backend",
        "full stack",
        "react",
        "javascript",
    },
    "cloud": {
        "cloud computing",
        "cloud",
        "devops",
        "deployment",
        "infrastructure",
    },
    "cybersecurity": {
        "cybersecurity",
        "cyber security",
        "security",
        "ethical hacking",
        "network security",
    },
    "design": {
        "ui design",
        "ux design",
        "ui/ux",
        "design",
        "product design",
        "user experience",
        "user interface",
    },
    "iot": {
        "iot",
        "internet of things",
        "embedded systems",
        "electronics",
        "robotics",
    },
    "programming": {
        "programming",
        "software development",
        "coding",
        "computer science",
    },
}


def clean_text(value: str) -> str:
    value = (value or "").strip().lower()
    value = value.replace("_", " ")
    value = value.replace("-", " ")
    value = re.sub(r"\s+", " ", value)
    return value


def parse_list_field(value):
    if isinstance(value, list):
        return value
    if not value:
        return []
    import json

    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, ValueError):
        return [value] if isinstance(value, str) and value.strip() else []


def normalize_skill(skill: str) -> str:
    cleaned = clean_text(skill)
    if cleaned in SKILL_ALIASES:
        return SKILL_ALIASES[cleaned]
    compact = cleaned.replace(" ", "")
    if compact in SKILL_ALIASES:
        return SKILL_ALIASES[compact]
    return cleaned


def normalize_branch(branch: str) -> str:
    cleaned = clean_text(branch)
    aliases = {
        "cse aiml": "cse-aiml",
        "cse ai ml": "cse-aiml",
        "computer science and engineering aiml": "cse-aiml",
        "computer science engineering": "cse",
        "computer science": "cse",
        "information technology": "it",
        "artificial intelligence and data science": "ai-ds",
        "ai and data science": "ai-ds",
    }
    return aliases.get(cleaned, cleaned)


def parse_student_year(value) -> int:
    if value in (None, ""):
        return 0
    if isinstance(value, int):
        return value
    match = re.search(r"\d+", str(value))
    return int(match.group()) if match else 0


def get_interest_group(value: str):
    cleaned = clean_text(value)
    for group, terms in INTEREST_GROUPS.items():
        for term in terms:
            if cleaned == term or cleaned in term or term in cleaned:
                return group
    normalized = normalize_skill(value)
    for group, terms in INTEREST_GROUPS.items():
        for term in terms:
            if normalized == term or normalized in term or term in normalized:
                return group
    return None


def split_location_preferences(location: str):
    if not location:
        return []
    parts = re.split(r",|/|\||\bor\b", clean_text(location))
    return [part.strip() for part in parts if part.strip()]


def calculate_skill_match(student: Student, opportunity: Opportunity):
    student_skills = parse_list_field(student.skills)
    required_skills = parse_list_field(opportunity.required_skills)
    preferred_skills = parse_list_field(opportunity.preferred_skills)

    student_skill_map = {normalize_skill(skill): skill for skill in student_skills}
    required_normalized = [normalize_skill(skill) for skill in required_skills]
    preferred_normalized = [normalize_skill(skill) for skill in preferred_skills]

    if not required_normalized and not preferred_normalized:
        return {
            "score": SKILL_WEIGHT,
            "matching_skills": [],
            "skill_gaps": [],
            "preferred_skill_gaps": [],
            "required_match_ratio": 1.0,
            "preferred_match_ratio": 1.0,
            "message": "No specific technical skills are required.",
        }

    matching_required = [student_skill_map[skill] for skill in required_normalized if skill in student_skill_map]
    required_match_ratio = len(matching_required) / len(required_normalized) if required_normalized else 1.0

    matching_preferred = [student_skill_map[skill] for skill in preferred_normalized if skill in student_skill_map]
    preferred_match_ratio = len(matching_preferred) / len(preferred_normalized) if preferred_normalized else 1.0

    skill_gaps = [skill for skill, norm in zip(required_skills, required_normalized) if norm not in student_skill_map]
    preferred_skill_gaps = [skill for skill, norm in zip(preferred_skills, preferred_normalized) if norm not in student_skill_map]

    skill_ratio = (required_match_ratio * 0.8) + (preferred_match_ratio * 0.2)
    skill_score = SKILL_WEIGHT * skill_ratio

    return {
        "score": round(skill_score, 2),
        "matching_skills": matching_required + matching_preferred,
        "skill_gaps": skill_gaps,
        "preferred_skill_gaps": preferred_skill_gaps,
        "required_match_ratio": round(required_match_ratio, 2),
        "preferred_match_ratio": round(preferred_match_ratio, 2),
        "message": f"Matched {len(matching_required)} of {len(required_normalized)} required skills.",
    }


def get_opportunity_interest_groups(opportunity: Opportunity):
    values = [opportunity.category, opportunity.title]
    values.extend(opportunity.required_skills or [])
    values.extend(opportunity.preferred_skills or [])
    groups = set()
    for value in values:
        group = get_interest_group(value)
        if group:
            groups.add(group)
    return groups


def calculate_interest_match(student: Student, opportunity: Opportunity):
    student_interests = parse_list_field(student.interests)
    if not student_interests:
        return {"score": 0, "matching_interests": [], "message": "No interests were provided."}

    student_groups = {}
    for interest in student_interests:
        group = get_interest_group(interest)
        if group:
            student_groups[group] = interest

    opportunity_groups = get_opportunity_interest_groups(opportunity)
    matching_groups = set(student_groups.keys()).intersection(opportunity_groups)
    matching_interests = [student_groups[group] for group in matching_groups]

    interest_ratio = len(matching_groups) / len(student_groups) if student_groups else 0
    interest_score = INTEREST_WEIGHT * interest_ratio

    return {
        "score": round(interest_score, 2),
        "matching_interests": matching_interests,
        "message": f"Matched {len(matching_interests)} of {len(student_groups)} interest areas.",
    }


def calculate_eligibility(student: Student, opportunity: Opportunity):
    student_year = parse_student_year(student.year)
    student_branch = normalize_branch(student.branch)
    opportunity_min_year = opportunity.min_year
    opportunity_max_year = opportunity.max_year
    eligible_branches = json_loads(opportunity.eligible_branches) if opportunity.eligible_branches else []

    year_eligible = True
    if opportunity_min_year is not None and student_year < opportunity_min_year:
        year_eligible = False
    if opportunity_max_year is not None and student_year > opportunity_max_year:
        year_eligible = False

    if not eligible_branches:
        branch_eligible = True
    elif any(clean_text(branch) == "all" for branch in eligible_branches):
        branch_eligible = True
    else:
        normalized_branches = [normalize_branch(branch) for branch in eligible_branches]
        branch_eligible = student_branch in normalized_branches

    eligible = year_eligible and branch_eligible
    reasons = []
    reasons.append("year requirement satisfied" if year_eligible else "year requirement not satisfied")
    reasons.append("branch requirement satisfied" if branch_eligible else "branch requirement not satisfied")
    return {
        "score": ELIGIBILITY_WEIGHT if eligible else 0,
        "eligible": eligible,
        "year_eligible": year_eligible,
        "branch_eligible": branch_eligible,
        "message": ", ".join(reasons),
    }


def json_loads(value):
    if not value:
        return []
    import json
    try:
        data = json.loads(value)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def calculate_location_match(student: Student, opportunity: Opportunity):
    preferred_location = student.preferred_location or "Any"
    opportunity_location = clean_text(opportunity.location or "")
    preferences = split_location_preferences(preferred_location)

    if not preferences or any(pref in {"any", "anywhere", "no preference"} for pref in preferences):
        return {"score": LOCATION_WEIGHT, "matched": True, "message": "Student has no location restriction."}

    for preference in preferences:
        if preference in {"remote", "online"}:
            if "remote" in opportunity_location or "online" in opportunity_location:
                return {"score": LOCATION_WEIGHT, "matched": True, "message": "Remote/online preference matches."}
        elif preference in opportunity_location or opportunity_location in preference:
            return {"score": LOCATION_WEIGHT, "matched": True, "message": "Preferred location matches."}

    return {"score": 0, "matched": False, "message": "Preferred location does not match."}


def calculate_category_match(student: Student, opportunity: Opportunity):
    preferred_categories = parse_list_field(student.preferred_categories)
    if not preferred_categories:
        return {"score": CATEGORY_WEIGHT, "matched": True, "message": "No category preference specified."}
    opportunity_category = clean_text(opportunity.category)
    for category in preferred_categories:
        normalized_category = clean_text(category)
        if normalized_category == opportunity_category or normalized_category in opportunity_category or opportunity_category in normalized_category:
            return {"score": CATEGORY_WEIGHT, "matched": True, "message": "Preferred category matches."}
    return {"score": 0, "matched": False, "message": "Preferred category does not match."}


def generate_explanation(skill_result, interest_result, eligibility_result, location_result, category_result, total_score):
    if not eligibility_result["eligible"]:
        return "This opportunity has relevant characteristics, but the profile does not currently satisfy all eligibility requirements."

    parts = []
    matching_skills = skill_result["matching_skills"]
    if matching_skills:
        if len(matching_skills) >= 3:
            parts.append(f"strong skill alignment with {', '.join(matching_skills[:3])}")
        else:
            parts.append(f"skill alignment with {', '.join(matching_skills)}")

    matching_interests = interest_result["matching_interests"]
    if matching_interests:
        parts.append(f"interest alignment in {', '.join(matching_interests[:2])}")
    if location_result["matched"]:
        parts.append("a matching location preference")
    if category_result["matched"]:
        parts.append("a matching opportunity category")
    if not parts:
        return f"The overall profile match is {total_score:.1f}% based on the available profile information."
    return f"This opportunity matches your profile through {'; '.join(parts)}."


def calculate_match(student: Student, opportunity: Opportunity):
    skill_result = calculate_skill_match(student, opportunity)
    interest_result = calculate_interest_match(student, opportunity)
    eligibility_result = calculate_eligibility(student, opportunity)
    location_result = calculate_location_match(student, opportunity)
    category_result = calculate_category_match(student, opportunity)

    total_score = (
        skill_result["score"]
        + interest_result["score"]
        + eligibility_result["score"]
        + location_result["score"]
        + category_result["score"]
    )
    total_score = round(max(0, min(100, total_score)), 1)

    explanation = generate_explanation(
        skill_result,
        interest_result,
        eligibility_result,
        location_result,
        category_result,
        total_score,
    )

    return {
        "match_percentage": total_score,
        "matching_skills": skill_result["matching_skills"],
        "skill_gaps": skill_result["skill_gaps"],
        "preferred_skill_gaps": skill_result["preferred_skill_gaps"],
        "matching_interests": interest_result["matching_interests"],
        "eligible": eligibility_result["eligible"],
        "score_breakdown": {
            "skills": skill_result["score"],
            "interests": interest_result["score"],
            "eligibility": eligibility_result["score"],
            "location": location_result["score"],
            "category": category_result["score"],
        },
        "eligibility_details": {
            "eligible": eligibility_result["eligible"],
            "year_eligible": eligibility_result["year_eligible"],
            "branch_eligible": eligibility_result["branch_eligible"],
        },
        "explanation": explanation,
    }


def recommend_opportunities(student: Student, opportunities):
    recommendations = []
    for opportunity in opportunities:
        match_result = calculate_match(student, opportunity)
        recommendations.append({"opportunity": opportunity, **match_result})
    recommendations.sort(key=lambda item: item["match_percentage"], reverse=True)
    return recommendations
