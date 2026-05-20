"""
GitHub REST API client — fetches public profile data, repos, and language stats.
No auth token required for public data (60 req/hr unauthenticated, 5000 with token).
"""
import os
import logging
from collections import Counter
import httpx

logger = logging.getLogger("github_api")

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


async def fetch_github_profile(username: str) -> dict:
    """
    Fetches full GitHub profile: user info + top repos + aggregated language stats.
    Returns a structured dict or raises ValueError on bad username / API errors.
    """
    async with httpx.AsyncClient(timeout=15, headers=_headers()) as client:
        # ── 1. User profile ──────────────────────────────────────────────────
        profile_res = await client.get(f"{GITHUB_API}/users/{username}")
        if profile_res.status_code == 404:
            raise ValueError(f"GitHub user '{username}' not found.")
        if profile_res.status_code == 403:
            raise ValueError("GitHub API rate limit hit. Add a GITHUB_TOKEN in .env.")
        if profile_res.status_code != 200:
            raise ValueError(f"GitHub API error {profile_res.status_code}.")

        profile = profile_res.json()

        # ── 2. Repositories (sorted by stars, up to 100) ─────────────────────
        repos_res = await client.get(
            f"{GITHUB_API}/users/{username}/repos",
            params={"sort": "stars", "direction": "desc", "per_page": 100, "type": "owner"},
        )
        repos_raw = repos_res.json() if repos_res.status_code == 200 else []

        # Skip forks for cleaner data
        own_repos = [r for r in repos_raw if not r.get("fork", False)]

        top_repos = []
        all_languages: list[str] = []
        total_stars = 0

        for r in own_repos:
            total_stars += r.get("stargazers_count", 0)
            if r.get("language"):
                all_languages.append(r["language"])
            if len(top_repos) < 6:
                top_repos.append(
                    {
                        "name": r.get("name", ""),
                        "description": r.get("description") or "",
                        "stars": r.get("stargazers_count", 0),
                        "forks": r.get("forks_count", 0),
                        "language": r.get("language") or "—",
                        "url": r.get("html_url", ""),
                    }
                )

        lang_counter = Counter(all_languages)
        total_lang = sum(lang_counter.values()) or 1
        top_languages = [
            {"name": lang, "count": count, "pct": round(count / total_lang * 100, 1)}
            for lang, count in lang_counter.most_common(6)
        ]

        return {
            "username": username,
            "name": profile.get("name") or username,
            "avatar_url": profile.get("avatar_url", ""),
            "bio": profile.get("bio") or "",
            "location": profile.get("location") or "",
            "company": profile.get("company") or "",
            "blog": profile.get("blog") or "",
            "twitter": profile.get("twitter_username") or "",
            "public_repos": profile.get("public_repos", 0),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
            "total_stars": total_stars,
            "account_created": profile.get("created_at", "")[:10],
            "top_repos": top_repos,
            "top_languages": top_languages,
        }
