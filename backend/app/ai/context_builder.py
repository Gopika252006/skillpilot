from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import User, KnowledgeConcept, CodeAnalysis, WeeklyPlan, UserProfile

def build_user_technical_context(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Extracts the user's personal technical memory profile to provide grounding
    for all AI operations.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {
            "target_role": "Software Engineer",
            "experience_level": "Intermediate",
            "strong_concepts": [],
            "weak_concepts": [],
            "repeated_mistakes": [],
            "recent_analyses": [],
            "current_focus": "Algorithms & System Design",
            "context_badges": ["General Developer Profile"]
        }

    profile = user.profile
    target_role = profile.target_role if profile else "Software Engineer"
    experience_level = profile.experience_level if profile else "Intermediate"
    interests = profile.interests if profile else ["DSA", "System Design"]

    # Knowledge concepts
    concepts = db.query(KnowledgeConcept).filter(KnowledgeConcept.user_id == user_id).all()
    
    strong_concepts = [
        f"{c.name} ({int(c.confidence * 100)}% conf, {c.practice_count}x practiced)" 
        for c in concepts if c.status == "STRONG" or c.confidence >= 0.8
    ]
    
    weak_concepts = [
        f"{c.name} ({c.status}, {int(c.confidence * 100)}% conf)" 
        for c in concepts if c.status in ["NEEDS_REVISION", "LEARNING"] or c.confidence < 0.6
    ]

    all_mistakes = []
    for c in concepts:
        for m in c.repeated_mistakes:
            if m not in all_mistakes:
                all_mistakes.append(f"{c.name}: {m}")

    # Recent code analyses
    recent_analyses = db.query(CodeAnalysis).filter(
        CodeAnalysis.user_id == user_id
    ).order_by(CodeAnalysis.created_at.desc()).limit(3).all()
    
    recent_problems = [
        f"{a.problem_title} ({a.language}, {a.approach_detected}, {a.time_complexity})"
        for a in recent_analyses
    ]

    # Active weekly plan
    active_plan = db.query(WeeklyPlan).filter(
        WeeklyPlan.user_id == user_id, 
        WeeklyPlan.is_active == True
    ).first()
    current_focus = active_plan.focus_area if active_plan else "Core Algorithms & Problem Solving"

    # Badges for UI context indicators
    context_badges = []
    if target_role:
        context_badges.append(f"Target: {target_role}")
    if current_focus:
        context_badges.append(f"Focus: {current_focus}")
    if weak_concepts:
        context_badges.append(f"Addressing: {weak_concepts[0].split(' ')[0]}")
    if recent_problems:
        context_badges.append(f"Recent: {recent_problems[0].split(' (')[0]}")

    context_prompt = f"""
[USER'S PERSONAL TECHNICAL MEMORY PROFILE]
* Target Career Role: {target_role} ({experience_level})
* Core Technical Interests: {', '.join(interests) if interests else 'General'}
* Known Strong Areas (proven practice): {', '.join(strong_concepts[:6]) if strong_concepts else 'None recorded yet'}
* Current Weak Areas / Needs Revision: {', '.join(weak_concepts[:6]) if weak_concepts else 'None recorded yet'}
* Recurring Mistakes & Blind Spots: {'; '.join(all_mistakes[:4]) if all_mistakes else 'None logged'}
* Current Weekly Focus: {current_focus}
* Recent Problem Solving: {'; '.join(recent_problems) if recent_problems else 'None yet'}
[END OF PERSONAL CONTEXT]
""".strip()

    return {
        "target_role": target_role,
        "experience_level": experience_level,
        "interests": interests,
        "strong_concepts": strong_concepts,
        "weak_concepts": weak_concepts,
        "repeated_mistakes": all_mistakes,
        "recent_analyses": recent_problems,
        "current_focus": current_focus,
        "context_badges": context_badges,
        "prompt_block": context_prompt
    }
