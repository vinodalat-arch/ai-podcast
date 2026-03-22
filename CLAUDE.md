# AI Podcast Platform

## What This Is
A Streamlit video podcast platform hosting a 15-episode AI thought-leadership series.
Central philosophy: **Software engineering is shifting from code → context → trust → systems.**

Full spec: `streamlit_video_podcast_project_brief_v2.md`

## Tech Stack
- Python + Streamlit
- Markdown/YAML content files (no database)
- Deployment: Render

## Project Structure
```
app.py                  # Main Streamlit app
requirements.txt
render.yaml
.streamlit/config.toml
content/
  episodes/             # Markdown files with YAML frontmatter (one per episode)
  thumbnails/           # Episode thumbnail images
components/             # Streamlit UI components
utils/                  # Content loader, helpers
assets/                 # Static assets (CSS, images, branding)
input/                  # Raw source material (NOT served by the app)
  arc1-4/
    videos/             # Video files provided by user
    whitepapers/        # PDF/DOCX whitepapers provided by user
```

## Content Model
Each episode is a markdown file in `content/episodes/` with YAML frontmatter:
- title, slug, episode_number, arc, video_url, thumbnail, tags
- publish_date, status, featured, summary
- Body = long-form description

Adding a new episode = add one markdown file + optional thumbnail. No code changes.

## Arc Structure (4 arcs, 15 episodes)
- **Arc 1: The Shift** — Ep 1-4 (breaking old mental models)
- **Arc 2: The New Engineering Model** — Ep 5-9 (context-centric engineering)
- **Arc 3: The Reality Check** — Ep 10-13 (enterprise friction)
- **Arc 4: The Future** — Ep 14-15 (what's next)

## Content Pipeline
User provides per episode: a whitepaper (PDF/DOCX) + a video file in `input/` folders.
Claude extracts content from whitepapers to generate episode markdown files.
Videos are hosted externally (YouTube/Vimeo) or locally — embed URL goes in frontmatter.

## Key Principles
- Content-driven, not hardcoded
- Arc structure is first-class (visible in nav, homepage, episode pages)
- Simple > over-engineered
- No database, no auth, no CMS
- Must feel like a credible, publishable platform — not a demo

## Commands
```bash
# Run locally
streamlit run app.py

# Deploy on Render
# Uses render.yaml — see deployment section in brief
```
