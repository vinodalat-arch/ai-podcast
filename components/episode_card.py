import streamlit as st
from utils.content_loader import ARCS


def render_episode_card(episode):
    """Render a single episode card — mobile-friendly, full width."""
    arc = episode.get("arc", "")
    arc_info = ARCS.get(arc, {})
    arc_color = arc_info.get("color", "#888")
    ep_num = episode.get("episode_number", 0)
    title = episode.get("title", "Untitled")
    summary = episode.get("summary", "")
    slug = episode.get("slug", "")
    tags = episode.get("tags", [])

    st.markdown(
        f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-left: 4px solid {arc_color};
            border-radius: 8px;
            padding: 16px 16px 12px 16px;
            margin-bottom: 8px;
            background: white;
        ">
            <div style="
                font-size: 12px;
                color: {arc_color};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 6px;
            ">
                Episode {ep_num} &middot; {arc}
            </div>
            <div style="
                font-size: 16px;
                font-weight: 700;
                color: #1a1a1a;
                margin-bottom: 6px;
                line-height: 1.3;
            ">
                {title}
            </div>
            <div style="
                font-size: 14px;
                color: #555;
                line-height: 1.5;
                margin-bottom: 10px;
            ">
                {summary}
            </div>
            <div style="font-size: 12px; color: #999;">
                {' &middot; '.join(tags[:4])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        f"▶ Watch Episode {ep_num}",
        key=f"card_{slug}",
        use_container_width=True,
    ):
        st.session_state["selected_episode"] = slug
        st.rerun()


def render_featured_card(episode):
    """Render a larger featured episode card."""
    arc = episode.get("arc", "")
    arc_info = ARCS.get(arc, {})
    arc_color = arc_info.get("color", "#888")
    ep_num = episode.get("episode_number", 0)
    title = episode.get("title", "Untitled")
    summary = episode.get("summary", "")
    slug = episode.get("slug", "")

    st.markdown(
        f"""
        <div style="
            border: 2px solid {arc_color};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
        ">
            <div style="
                font-size: 11px;
                color: {arc_color};
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            ">
                &#9733; Featured &middot; Episode {ep_num} &middot; {arc}
            </div>
            <div style="
                font-size: 22px;
                font-weight: 800;
                color: #1a1a1a;
                margin-bottom: 10px;
                line-height: 1.2;
            ">
                {title}
            </div>
            <div style="
                font-size: 15px;
                color: #444;
                line-height: 1.6;
            ">
                {summary}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "▶ Watch Featured Episode",
        key=f"featured_{slug}",
        use_container_width=True,
    ):
        st.session_state["selected_episode"] = slug
        st.rerun()
