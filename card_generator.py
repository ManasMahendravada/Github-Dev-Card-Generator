"""
Card generator — produces a stunning, self-contained HTML dev card.
Each theme is a full visual identity (colors, gradients, typography accents).
"""
import html as html_lib
from pathlib import Path

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "hacker": {
        "bg": "#0d0d0d",
        "card_bg": "#111827",
        "border": "#00ff41",
        "text": "#e5e7eb",
        "subtext": "#9ca3af",
        "accent": "#00ff41",
        "accent2": "#00cc33",
        "badge_bg": "rgba(0,255,65,0.15)",
        "badge_text": "#00ff41",
        "stat_bg": "rgba(0,255,65,0.08)",
        "repo_bg": "rgba(0,255,65,0.05)",
        "gradient": "linear-gradient(135deg, #0d0d0d 0%, #0a1f0a 100%)",
        "header_gradient": "linear-gradient(135deg, #0d1f0d 0%, #001a00 100%)",
        "font": "'Courier New', Courier, monospace",
        "emoji": "🖥️",
        "label": "H4CK3R",
        "glow": "0 0 20px rgba(0,255,65,0.3)",
    },
    "builder": {
        "bg": "#0f172a",
        "card_bg": "#1e293b",
        "border": "#3b82f6",
        "text": "#f1f5f9",
        "subtext": "#94a3b8",
        "accent": "#3b82f6",
        "accent2": "#60a5fa",
        "badge_bg": "rgba(59,130,246,0.15)",
        "badge_text": "#60a5fa",
        "stat_bg": "rgba(59,130,246,0.08)",
        "repo_bg": "rgba(59,130,246,0.05)",
        "gradient": "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)",
        "header_gradient": "linear-gradient(135deg, #1e3a5f 0%, #1e1b4b 100%)",
        "font": "'Inter', 'Segoe UI', sans-serif",
        "emoji": "🔨",
        "label": "BUILDER",
        "glow": "0 0 20px rgba(59,130,246,0.3)",
    },
    "researcher": {
        "bg": "#1a0f2e",
        "card_bg": "#231940",
        "border": "#a78bfa",
        "text": "#f3f0ff",
        "subtext": "#c4b5fd",
        "accent": "#a78bfa",
        "accent2": "#c4b5fd",
        "badge_bg": "rgba(167,139,250,0.15)",
        "badge_text": "#c4b5fd",
        "stat_bg": "rgba(167,139,250,0.08)",
        "repo_bg": "rgba(167,139,250,0.05)",
        "gradient": "linear-gradient(135deg, #1a0f2e 0%, #2d1b69 100%)",
        "header_gradient": "linear-gradient(135deg, #2d1b69 0%, #1a0f2e 100%)",
        "font": "'Georgia', 'Times New Roman', serif",
        "emoji": "🔬",
        "label": "RESEARCHER",
        "glow": "0 0 20px rgba(167,139,250,0.3)",
    },
    "designer": {
        "bg": "#1a0a1e",
        "card_bg": "#2d1032",
        "border": "#ec4899",
        "text": "#fdf4ff",
        "subtext": "#f0abfc",
        "accent": "#ec4899",
        "accent2": "#f472b6",
        "badge_bg": "rgba(236,72,153,0.15)",
        "badge_text": "#f472b6",
        "stat_bg": "rgba(236,72,153,0.08)",
        "repo_bg": "rgba(236,72,153,0.05)",
        "gradient": "linear-gradient(135deg, #1a0a1e 0%, #3b0764 100%)",
        "header_gradient": "linear-gradient(135deg, #831843 0%, #3b0764 100%)",
        "font": "'Inter', 'Helvetica Neue', sans-serif",
        "emoji": "🎨",
        "label": "DESIGNER",
        "glow": "0 0 20px rgba(236,72,153,0.3)",
    },
    "open-source-hero": {
        "bg": "#0d1f0d",
        "card_bg": "#14290f",
        "border": "#22c55e",
        "text": "#f0fdf4",
        "subtext": "#86efac",
        "accent": "#22c55e",
        "accent2": "#4ade80",
        "badge_bg": "rgba(34,197,94,0.15)",
        "badge_text": "#4ade80",
        "stat_bg": "rgba(34,197,94,0.08)",
        "repo_bg": "rgba(34,197,94,0.05)",
        "gradient": "linear-gradient(135deg, #0d1f0d 0%, #14532d 100%)",
        "header_gradient": "linear-gradient(135deg, #14532d 0%, #052e16 100%)",
        "font": "'Inter', 'Segoe UI', sans-serif",
        "emoji": "🦸",
        "label": "OSS HERO",
        "glow": "0 0 20px rgba(34,197,94,0.3)",
    },
}

# Language → color mapping
LANG_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#2b7489",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "C": "#555555",
    "C#": "#178600",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Swift": "#ffac45",
    "Kotlin": "#F18E33",
    "Dart": "#00B4AB",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Jupyter Notebook": "#DA5B0B",
    "R": "#198CE7",
    "Scala": "#c22d40",
    "Vue": "#41b883",
    "Svelte": "#ff3e00",
    "Lua": "#000080",
    "Haskell": "#5e5086",
    "Elixir": "#6e4a7e",
    "Clojure": "#db5855",
    "default": "#8b8b8b",
}


def _lang_color(lang: str) -> str:
    return LANG_COLORS.get(lang, LANG_COLORS["default"])


def _e(s) -> str:
    """HTML-escape a value."""
    return html_lib.escape(str(s) if s is not None else "")


def generate_card_html(username: str, github_data: dict, analysis: dict) -> str:
    """Generate a self-contained, beautiful HTML dev card."""
    theme_key = analysis.get("card_theme", "builder")
    if theme_key not in THEMES:
        theme_key = "builder"
    t = THEMES[theme_key]

    name = _e(github_data.get("name", username))
    bio = _e(github_data.get("bio", ""))
    location = _e(github_data.get("location", ""))
    company = _e(github_data.get("company", ""))
    avatar = _e(github_data.get("avatar_url", ""))
    repos = github_data.get("public_repos", 0)
    followers = github_data.get("followers", 0)
    following = github_data.get("following", 0)
    stars = github_data.get("total_stars", 0)
    joined = github_data.get("account_created", "")[:4]
    twitter = github_data.get("twitter", "")
    blog = github_data.get("blog", "")

    vibe = _e(analysis.get("developer_vibe", ""))
    skills = analysis.get("top_skills", [])
    fun_fact = _e(analysis.get("fun_fact", ""))
    level = _e(analysis.get("expertise_level", "Advanced"))
    superpower = _e(analysis.get("superpower", "Building great things"))
    achievement = _e(analysis.get("achievement", "Code Craftsman"))
    lang_summary = _e(analysis.get("languages_summary", ""))

    # Skills badges
    skills_html = "".join(
        f'<span style="background:{t["badge_bg"]};color:{t["badge_text"]};border:1px solid {t["accent"]}33;'
        f'padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;white-space:nowrap;">'
        f'{_e(s)}</span>'
        for s in skills
    )

    # Language bars
    lang_bars = ""
    for lang in github_data.get("top_languages", [])[:5]:
        color = _lang_color(lang["name"])
        lang_bars += (
            f'<div style="margin-bottom:8px;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:3px;">'
            f'<span style="font-size:12px;font-weight:600;color:{t["text"]};">{_e(lang["name"])}</span>'
            f'<span style="font-size:11px;color:{t["subtext"]};">{lang["pct"]}%</span>'
            f'</div>'
            f'<div style="background:rgba(255,255,255,0.08);border-radius:4px;height:6px;overflow:hidden;">'
            f'<div style="width:{lang["pct"]}%;height:100%;background:{color};border-radius:4px;'
            f'box-shadow:0 0 6px {color}66;"></div>'
            f'</div>'
            f'</div>'
        )

    # Top repos (first 3)
    repos_html = ""
    for r in github_data.get("top_repos", [])[:3]:
        lang_dot = f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{_lang_color(r["language"])};margin-right:4px;"></span>' if r.get("language") else ""
        repos_html += (
            f'<a href="{_e(r["url"])}" target="_blank" style="text-decoration:none;">'
            f'<div style="background:{t["repo_bg"]};border:1px solid {t["accent"]}22;border-radius:8px;'
            f'padding:10px 12px;margin-bottom:8px;transition:all 0.2s;cursor:pointer;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">'
            f'<span style="font-size:13px;font-weight:700;color:{t["accent2"]};">{_e(r["name"])}</span>'
            f'<span style="font-size:11px;color:{t["subtext"]};">⭐ {r["stars"]}</span>'
            f'</div>'
            f'<div style="font-size:11px;color:{t["subtext"]};margin-bottom:5px;line-height:1.4;">'
            f'{_e(r["description"][:80]) if r["description"] else "No description"}'
            f'</div>'
            f'<div style="font-size:11px;color:{t["subtext"]};">{lang_dot}{_e(r["language"])}</div>'
            f'</div>'
            f'</a>'
        )

    # Social links
    social_html = ""
    if blog:
        social_html += f'<a href="{_e(blog)}" target="_blank" style="color:{t["accent2"]};text-decoration:none;font-size:11px;margin-right:12px;">🌐 Website</a>'
    if twitter:
        social_html += f'<a href="https://twitter.com/{_e(twitter)}" target="_blank" style="color:{t["accent2"]};text-decoration:none;font-size:11px;">𝕏 @{_e(twitter)}</a>'

    card_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — GitHub Dev Card</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: {t["bg"]}; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; font-family: {t["font"]}; }}
  .card {{
    width: 420px;
    background: {t["card_bg"]};
    border: 1px solid {t["accent"]}44;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: {t["glow"]}, 0 20px 60px rgba(0,0,0,0.5);
    position: relative;
  }}
  .card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {t["accent"]}, {t["accent2"]}, transparent);
  }}
  .header {{
    background: {t["header_gradient"]};
    padding: 24px;
    position: relative;
    overflow: hidden;
  }}
  .header::after {{
    content: '{t["emoji"]}';
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 52px;
    opacity: 0.15;
  }}
  .avatar-row {{ display: flex; align-items: flex-start; gap: 16px; }}
  .avatar-wrap {{
    position: relative;
    flex-shrink: 0;
  }}
  .avatar {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    border: 2px solid {t["accent"]};
    box-shadow: 0 0 16px {t["accent"]}66;
    object-fit: cover;
  }}
  .level-badge {{
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    background: {t["accent"]};
    color: {t["bg"]};
    font-size: 8px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 8px;
    white-space: nowrap;
    letter-spacing: 0.5px;
  }}
  .name {{ font-size: 20px; font-weight: 800; color: {t["text"]}; line-height: 1.2; margin-bottom: 2px; }}
  .handle {{ font-size: 13px; color: {t["accent"]}; margin-bottom: 6px; }}
  .bio {{ font-size: 12px; color: {t["subtext"]}; line-height: 1.5; }}
  .meta {{ font-size: 11px; color: {t["subtext"]}; margin-top: 6px; display:flex;gap:12px;flex-wrap:wrap; }}
  .body {{ padding: 20px 24px; }}
  .vibe-box {{
    background: {t["stat_bg"]};
    border-left: 3px solid {t["accent"]};
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-bottom: 16px;
    font-size: 12px;
    color: {t["text"]};
    line-height: 1.5;
    font-style: italic;
  }}
  .section-label {{
    font-size: 10px;
    font-weight: 700;
    color: {t["accent"]};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .section-label::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {t["accent"]}22;
  }}
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 4px;
  }}
  .stat {{
    background: {t["stat_bg"]};
    border: 1px solid {t["accent"]}15;
    border-radius: 10px;
    padding: 10px 6px;
    text-align: center;
  }}
  .stat-value {{ font-size: 18px; font-weight: 800; color: {t["text"]}; line-height: 1; }}
  .stat-label {{ font-size: 9px; color: {t["subtext"]}; margin-top: 3px; font-weight: 600; letter-spacing: 0.5px; text-transform:uppercase; }}
  .skills-wrap {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .superpower {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, {t["accent"]}22, {t["accent2"]}11);
    border: 1px solid {t["accent"]}44;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 700;
    color: {t["accent2"]};
    margin-bottom: 4px;
  }}
  .achievement {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: {t["badge_bg"]};
    border: 1px solid {t["accent"]}44;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    color: {t["badge_text"]};
    margin-left: 8px;
  }}
  .fun-fact {{
    background: {t["stat_bg"]};
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 11px;
    color: {t["subtext"]};
    line-height: 1.5;
    margin-top: 4px;
  }}
  .footer {{
    padding: 12px 24px;
    border-top: 1px solid {t["accent"]}15;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .theme-tag {{
    font-size: 9px;
    font-weight: 800;
    color: {t["accent"]};
    letter-spacing: 2px;
    text-transform: uppercase;
    border: 1px solid {t["accent"]}44;
    padding: 3px 8px;
    border-radius: 4px;
  }}
  .joined {{ font-size: 10px; color: {t["subtext"]}; }}
  @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .card {{ animation: fadeIn 0.5s ease; }}
</style>
</head>
<body>
<div class="card">
  <!-- Header -->
  <div class="header">
    <div class="avatar-row">
      <div class="avatar-wrap">
        <img class="avatar" src="{avatar}" alt="{name}" onerror="this.src='https://github.com/ghost.png'">
        <div class="level-badge">{level}</div>
      </div>
      <div style="flex:1;min-width:0;">
        <div class="name">{name}</div>
        <div class="handle">@{_e(username)}</div>
        {f'<div class="bio">{bio}</div>' if bio else ''}
        <div class="meta">
          {f'<span>📍 {location}</span>' if location else ''}
          {f'<span>🏢 {company}</span>' if company else ''}
        </div>
      </div>
    </div>
  </div>

  <!-- Body -->
  <div class="body">
    <!-- Vibe -->
    <div class="vibe-box">"{vibe}"</div>

    <!-- Stats -->
    <div class="section-label">GitHub Stats</div>
    <div class="stats-grid">
      <div class="stat">
        <div class="stat-value">{repos}</div>
        <div class="stat-label">Repos</div>
      </div>
      <div class="stat">
        <div class="stat-value">{_format_num(followers)}</div>
        <div class="stat-label">Followers</div>
      </div>
      <div class="stat">
        <div class="stat-value">{_format_num(stars)}</div>
        <div class="stat-label">Stars</div>
      </div>
      <div class="stat">
        <div class="stat-value">{following}</div>
        <div class="stat-label">Following</div>
      </div>
    </div>

    <!-- Skills -->
    <div class="section-label">Top Skills</div>
    <div class="skills-wrap">{skills_html}</div>

    <!-- Superpower + Achievement -->
    <div class="section-label" style="margin-top:14px;">Highlights</div>
    <div>
      <div class="superpower">⚡ {superpower}</div>
      <span class="achievement">🏆 {achievement}</span>
    </div>

    <!-- Languages -->
    {f'<div class="section-label">Languages</div><div>{lang_bars}</div>' if lang_bars else ''}

    <!-- Top Repos -->
    {f'<div class="section-label">Pinned Repos</div><div>{repos_html}</div>' if repos_html else ''}

    <!-- Fun Fact -->
    {f'<div class="section-label">Fun Fact</div><div class="fun-fact">💡 {fun_fact}</div>' if fun_fact else ''}

    <!-- Social -->
    {f'<div style="margin-top:12px;">{social_html}</div>' if social_html else ''}
  </div>

  <!-- Footer -->
  <div class="footer">
    <div class="theme-tag">{t["label"]}</div>
    {f'<span class="joined">GitHub since {joined}</span>' if joined else ''}
    <a href="https://github.com/{_e(username)}" target="_blank"
       style="font-size:11px;color:{t["accent2"]};text-decoration:none;font-weight:600;">
      View Profile →
    </a>
  </div>
</div>
</body>
</html>"""
    return card_html


def _format_num(n: int) -> str:
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def save_card(username: str, html: str, base_dir: Path) -> str:
    """Save card HTML and return its relative URL path."""
    cards_dir = base_dir / "static" / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    file_path = cards_dir / f"{username}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    return f"/static/cards/{username}.html"
