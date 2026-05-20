"""
Gemini AI analysis via direct REST API — no SDK, works on Python 3.14+
API key is read inside functions so load_dotenv() has time to run first.
"""
import os
import json
import logging
import httpx

logger = logging.getLogger("gemini_api")

MODEL_NAME = "gemini-1.5-flash"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

ANALYSIS_PROMPT = """
You are a witty, insightful developer analyst. Analyze the GitHub profile data below and return ONLY a JSON object — no markdown fences, no extra text.

GitHub Data:
{data}

Return exactly this JSON structure:
{{
  "developer_vibe": "<one punchy sentence capturing this developer's personality and coding style>",
  "top_skills": ["<skill1>", "<skill2>", "<skill3>"],
  "fun_fact": "<one clever, specific observation inferred from their repos or stats>",
  "card_theme": "<exactly one of: hacker | builder | researcher | designer | open-source-hero>",
  "expertise_level": "<exactly one of: Beginner | Intermediate | Advanced | Expert | Legend>",
  "superpower": "<their single biggest technical superpower in 4-6 words>",
  "achievement": "<one specific achievement badge like '10K+ Stars Club' or 'Polyglot Dev' or 'Community Builder'>",
  "languages_summary": "<one sentence describing their language preferences>"
}}

Rules:
- card_theme MUST be one of: hacker, builder, researcher, designer, open-source-hero
- expertise_level MUST be one of: Beginner, Intermediate, Advanced, Expert, Legend
- Be specific and clever — base everything on the data provided
"""


async def analyze_github_profile(github_data: dict) -> dict:
    """
    Calls Gemini REST API. Reads API key at call time (after load_dotenv runs).
    Always falls back gracefully — never raises an exception to the caller.
    """
    # Read key here, NOT at module level, so load_dotenv() has already run
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        logger.warning("GOOGLE_API_KEY not found in .env — using smart fallback analysis.")
        return _fallback_analysis(github_data)

    trimmed = {
        "name": github_data.get("name"),
        "bio": github_data.get("bio"),
        "public_repos": github_data.get("public_repos"),
        "followers": github_data.get("followers"),
        "total_stars": github_data.get("total_stars"),
        "top_languages": github_data.get("top_languages", [])[:5],
        "top_repos": [
            {
                "name": r["name"],
                "stars": r["stars"],
                "language": r["language"],
                "description": r["description"][:120],
            }
            for r in github_data.get("top_repos", [])[:6]
        ],
        "account_created": github_data.get("account_created"),
    }

    prompt = ANALYSIS_PROMPT.format(data=json.dumps(trimmed, indent=2))
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 512,
            "responseMimeType": "application/json",
        },
    }

    url = GEMINI_URL.format(model=MODEL_NAME)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                url,
                params={"key": api_key},
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        if res.status_code == 400:
            logger.warning(f"Gemini 400 Bad Request: {res.text[:300]}")
            return _fallback_analysis(github_data)
        if res.status_code == 403:
            logger.warning("Gemini 403 — API key invalid or quota exceeded.")
            return _fallback_analysis(github_data)
        if res.status_code != 200:
            logger.warning(f"Gemini returned {res.status_code}: {res.text[:200]}")
            return _fallback_analysis(github_data)

        data = res.json()
        raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        analysis = json.loads(raw.strip())
        logger.info(f"[GEMINI] OK — theme={analysis.get('card_theme')}, level={analysis.get('expertise_level')}")
        return analysis

    except Exception as e:
        logger.warning(f"Gemini call failed ({e}) — using fallback.")
        return _fallback_analysis(github_data)


def _fallback_analysis(github_data: dict) -> dict:
    """Smart fallback when Gemini is unavailable — still produces great cards."""
    repos = github_data.get("public_repos", 0)
    stars = github_data.get("total_stars", 0)
    followers = github_data.get("followers", 0)
    langs = [l["name"] for l in github_data.get("top_languages", [])]

    if stars > 10000 or followers > 10000:
        theme, level, achievement = "open-source-hero", "Legend", "Open Source Legend"
    elif stars > 1000 or followers > 1000:
        theme, level, achievement = "open-source-hero", "Expert", "Rising Star"
    elif repos > 50:
        theme, level, achievement = "builder", "Expert", "Prolific Builder"
    elif "Python" in langs or "R" in langs or "Julia" in langs:
        theme, level, achievement = "researcher", "Advanced", "Data Wizard"
    elif "CSS" in langs or "SCSS" in langs:
        theme, level, achievement = "designer", "Advanced", "Design Thinker"
    elif "C" in langs or "Rust" in langs or "Assembly" in langs:
        theme, level, achievement = "hacker", "Expert", "Systems Whisperer"
    else:
        theme, level, achievement = "builder", "Advanced", "Code Craftsman"

    primary = langs[0] if langs else "code"
    top3 = langs[:3] if langs else ["Problem Solving", "Clean Code", "Collaboration"]

    return {
        "developer_vibe": f"A passionate {primary} developer with {repos} repos and {stars} stars to their name.",
        "top_skills": top3,
        "fun_fact": f"With {repos} public repos and {stars} total stars, this developer clearly ships often and ships well.",
        "card_theme": theme,
        "expertise_level": level,
        "superpower": f"Building great things with {primary}",
        "achievement": achievement,
        "languages_summary": f"Primarily works in {', '.join(top3)}." if langs else "A versatile polyglot developer.",
    }
