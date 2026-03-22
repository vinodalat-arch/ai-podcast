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
    industry_quote = episode.get("industry_quote", "")
    quote_author = episode.get("quote_author", "")

    st.markdown(
        f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-left: 4px solid {arc_color};
            border-radius: 8px;
            padding: 16px 16px 12px 16px;
            margin-bottom: 8px;
            background: white;
            display: flex;
            gap: 14px;
            align-items: flex-start;
        ">
            <div style="
                background: {arc_color};
                color: white;
                font-weight: 800;
                font-size: 13px;
                padding: 6px 10px;
                border-radius: 6px;
                white-space: nowrap;
                min-width: 42px;
                text-align: center;
                flex-shrink: 0;
            ">
                E{ep_num:02d}
            </div>
            <div style="flex: 1;">
                <div style="
                    font-size: 12px;
                    color: {arc_color};
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 4px;
                ">
                    {arc}
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
                    margin-bottom: 8px;
                ">
                    {summary}
                </div>
                <div style="font-size: 12px; color: #999; margin-bottom: 6px;">
                    {' &middot; '.join(tags[:4])}
                </div>
                {f'<div style="font-size:12px;color:#888;font-style:italic;border-left:2px solid {arc_color};padding-left:8px;margin-top:4px;">"{industry_quote}" <span style="color:#aaa;">— {quote_author}</span></div>' if industry_quote else ''}
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
