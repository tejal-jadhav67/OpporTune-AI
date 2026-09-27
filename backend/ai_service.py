import json
import os

from dotenv import load_dotenv

load_dotenv()


def parse_list(value):
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, ValueError):
        return []


def generate_opportunity_explanation(student, opportunity, match_result):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, timeout=15.0)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        student_skills = parse_list(student.skills)
        student_interests = parse_list(student.interests)
        required_skills = parse_list(opportunity.required_skills)
        preferred_skills = parse_list(opportunity.preferred_skills)

        prompt = f"""You are an AI career opportunity assistant.

Write a concise, personalized explanation in 2 to 4 plain-text sentences for why this opportunity matches the student.

Rules:
- Do not calculate or change the match percentage.
- Use only the supplied facts. Do not invent qualifications, deadlines, or promises.
- Mention strengths first and important skill gaps honestly.
- Clearly state if the student is not eligible.
- Do not use markdown.

Student:
Name: {student.name or 'the student'}
Education: {student.education}
Year: {student.year}
Branch: {student.branch}
Skills: {student_skills}
Interests: {student_interests}

Opportunity:
Title: {opportunity.title}
Organization: {opportunity.organization}
Category: {opportunity.category}
Description: {opportunity.description}
Required skills: {required_skills}
Preferred skills: {preferred_skills}
Eligibility: {opportunity.eligibility}
Location: {opportunity.location}

Deterministic result:
Match percentage: {match_result.get('match_percentage', 0)}%
Matching skills: {match_result.get('matching_skills', [])}
Skill gaps: {match_result.get('skill_gaps', [])}
Preferred skill gaps: {match_result.get('preferred_skill_gaps', [])}
Matching interests: {match_result.get('matching_interests', [])}
Eligible: {match_result.get('eligible', False)}
Score breakdown: {match_result.get('score_breakdown', {})}

Write the explanation now."""

        response = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=150,
        )
        explanation = (response.output_text or "").strip()
        return explanation or None
    except Exception as error:
        print(f"AI explanation error: {error}")
        return None
