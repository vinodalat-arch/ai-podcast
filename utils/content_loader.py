import os
import yaml
import glob
import streamlit as st


CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "episodes")

ARCS = {
    "The Shift": {
        "order": 1,
        "description": "Breaking old mental models — challenging assumptions about code, frameworks, models, and correctness.",
        "color": "#E74C3C",
    },
    "The New Engineering Model": {
        "order": 2,
        "description": "Replacing the old worldview with context-centric engineering, AI-native architecture, and new roles.",
        "color": "#3498DB",
    },
    "The Reality Check": {
        "order": 3,
        "description": "Grounding ideas in enterprise reality — control, cost, compliance, and organizational friction.",
        "color": "#F39C12",
    },
    "The Future": {
        "order": 4,
        "description": "Where this leads — AI as the development operating system and the path from requirements to execution.",
        "color": "#2ECC71",
    },
}


def parse_episode(filepath):
    """Parse a markdown episode file with YAML frontmatter."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    metadata["body"] = parts[2].strip()
    metadata["file"] = os.path.basename(filepath)
    return metadata


@st.cache_data(ttl=60)
def load_all_episodes(include_drafts=False):
    """Load all episode files, sorted by episode number."""
    episodes = []
    pattern = os.path.join(CONTENT_DIR, "*.md")

    for filepath in glob.glob(pattern):
        episode = parse_episode(filepath)
        if episode is None:
            continue
        if not include_drafts and episode.get("status") != "published":
            continue
        episodes.append(episode)

    episodes.sort(key=lambda e: e.get("episode_number", 999))
    return episodes


def get_episode_by_slug(slug, include_drafts=False):
    """Get a single episode by slug."""
    for episode in load_all_episodes(include_drafts):
        if episode.get("slug") == slug:
            return episode
    return None


def get_episodes_by_arc(arc_name, include_drafts=False):
    """Get all episodes in a given arc."""
    return [e for e in load_all_episodes(include_drafts) if e.get("arc") == arc_name]


def get_featured_episodes(include_drafts=False):
    """Get featured episodes."""
    return [e for e in load_all_episodes(include_drafts) if e.get("featured")]


def get_all_tags(include_drafts=False):
    """Get all unique tags across episodes."""
    tags = set()
    for episode in load_all_episodes(include_drafts):
        for tag in episode.get("tags", []):
            tags.add(tag)
    return sorted(tags)


def get_related_episodes(episode, include_drafts=False):
    """Get related episodes — same arc, excluding self."""
    return [
        e for e in load_all_episodes(include_drafts)
        if e.get("arc") == episode.get("arc")
        and e.get("episode_number") != episode.get("episode_number")
    ]


def get_adjacent_episodes(episode, include_drafts=False):
    """Get previous and next episodes by episode number."""
    all_eps = load_all_episodes(include_drafts)
    ep_num = episode.get("episode_number", 0)
    prev_ep = None
    next_ep = None

    for e in all_eps:
        n = e.get("episode_number", 0)
        if n < ep_num:
            if prev_ep is None or n > prev_ep.get("episode_number", 0):
                prev_ep = e
        elif n > ep_num:
            if next_ep is None or n < next_ep.get("episode_number", 0):
                next_ep = e

    return prev_ep, next_ep
