# AI Podcast Platform

## What This Is
A Streamlit video podcast platform hosting a 15-episode AI thought-leadership series.
Central philosophy: **Software engineering is shifting from code → context → trust → systems.**

Full spec: `streamlit_video_podcast_project_brief_v2.md`

## Tech Stack
- Python + Streamlit
- Markdown/YAML content files (no database)
- Deployment: Streamlit Community Cloud
- GitHub: vinodalat-arch/ai-podcast

## Project Structure
```
app.py                  # Main Streamlit app
requirements.txt
.streamlit/config.toml
.claude/                # Skills, settings, hooks
content/
  episodes/             # Markdown files with YAML frontmatter (one per episode)
  thumbnails/           # Episode thumbnail images
components/             # Streamlit UI components
utils/                  # Content loader, helpers
assets/                 # Static assets (CSS, images, branding)
input/                  # Raw source material (gitignored, NOT in repo)
  arc1-4/
    videos/             # Video files provided by user
    whitepapers/        # PDF/DOCX whitepapers provided by user
```

## Content Model
Each episode is a markdown file in `content/episodes/` with YAML frontmatter:
- title, slug, episode_number, arc, video_url, thumbnail, tags
- publish_date, status, featured, builds_on, summary
- industry_quote, quote_author
- Body = show-notes style prose (no section labels)

Adding a new episode: use `/add-episode [whitepaper-path] [video-url]`

## Arc Structure (4 arcs, 15 episodes)
- **Arc 1: The Shift** — Ep 1-4 (breaking old mental models) — PUBLISHED
- **Arc 2: The New Engineering Model** — Ep 5-9 (context-centric engineering)
- **Arc 3: The Reality Check** — Ep 10-13 (enterprise friction)
- **Arc 4: The Future** — Ep 14-15 (what's next)

## Content Pipeline
User provides per episode: a whitepaper (PDF/DOCX) + a video (Google Drive link).
Claude extracts content from whitepapers to generate episode markdown files.
Videos are hosted on Google Drive (must be "Anyone with link can view").
Direct episode links: `?episode=slug-name` for LinkedIn sharing.

## Security Rules (MANDATORY)
- NEVER commit API keys, secrets, tokens, or credentials to the repo
- NEVER write to `.env`, `.pem`, or any credentials files
- NEVER hardcode sensitive data in code — use Streamlit Cloud Secrets if needed
- `input/` folder is gitignored — raw whitepapers and videos stay local only
- No database, no backend, no auth — nothing to expose
- Always verify `.gitignore` covers sensitive files before committing

## Key Principles
- Content-driven, not hardcoded
- Arc structure is first-class (visible in nav, homepage, episode pages)
- Simple > over-engineered
- No database, no auth, no CMS
- Mobile-first — most readers consume on phone
- Must feel like a credible, publishable platform — not a demo
- Clarity > features, narrative > UI complexity, simplicity > over-engineering

## Commands
```bash
# Run locally
streamlit run app.py --server.port 8510

# Auto-deploys on git push to main
git push
```
