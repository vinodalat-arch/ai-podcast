import streamlit as st
from utils.content_loader import ARCS, get_related_episodes, get_adjacent_episodes, get_episodes_by_arc


def render_video(video_url):
    """Render embedded video player."""
    if not video_url:
        st.info("Video coming soon.")
        return

    if "drive.google.com" in video_url:
        if "/d/" in video_url:
            file_id = video_url.split("/d/")[1].split("/")[0]
        else:
            file_id = video_url.split("id=")[1].split("&")[0]
        st.markdown(
            f'<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;">'
            f'<iframe src="https://drive.google.com/file/d/{file_id}/preview" '
            f'style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" '
            f'allowfullscreen></iframe></div>',
            unsafe_allow_html=True,
        )
    elif "youtube.com" in video_url or "youtu.be" in video_url:
        if "youtu.be/" in video_url:
            vid = video_url.split("youtu.be/")[-1].split("?")[0]
        else:
            vid = video_url.split("v=")[-1].split("&")[0]
        st.markdown(
            f'<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;">'
            f'<iframe src="https://www.youtube.com/embed/{vid}" '
            f'style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" '
            f'allowfullscreen></iframe></div>',
            unsafe_allow_html=True,
        )
    elif "vimeo.com" in video_url:
        vid = video_url.split("/")[-1]
        st.markdown(
            f'<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;">'
            f'<iframe src="https://player.vimeo.com/video/{vid}" '
            f'style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" '
            f'allowfullscreen></iframe></div>',
            unsafe_allow_html=True,
        )
    elif video_url.endswith((".mp4", ".mov", ".webm")):
        st.video(video_url)
    else:
        st.warning(f"Unsupported video format: {video_url}")


def render_episode_detail(episode):
    """Render full episode detail view."""
    arc = episode.get("arc", "")
    arc_info = ARCS.get(arc, {})
    arc_color = arc_info.get("color", "#888")
    ep_num = episode.get("episode_number", 0)
    title = episode.get("title", "Untitled")
    tags = episode.get("tags", [])
    body = episode.get("body", "")
    video_url = episode.get("video_url", "")

    # Back button
    if st.button("← Back to Episodes"):
        st.session_state["selected_episode"] = None
        st.rerun()

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # Header
    st.markdown(
        f'<div style="margin-bottom:8px;">'
        f'<span style="background:{arc_color};color:white;padding:4px 12px;'
        f'border-radius:20px;font-size:12px;font-weight:600;">{arc}</span>'
        f'<span style="color:#888;font-size:14px;margin-left:12px;">Episode {ep_num}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(f"# {title}")

    # Tags
    tag_html = " ".join(
        f'<span style="background:#f0f0f0;color:#555;padding:3px 10px;'
        f'border-radius:12px;font-size:12px;margin-right:6px;">{tag}</span>'
        for tag in tags
    )
    st.markdown(tag_html, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    # Video
    render_video(video_url)

    st.markdown(
        '<div style="text-align:right;font-size:12px;color:#999;margin-top:6px;">'
        'Video production assisted by NotebookLM'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # Body content
    st.markdown(body)

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    # --- Navigation Section ---
    st.markdown("### Continue")
    st.markdown("")

    # Previous / Next episode (overall)
    prev_ep, next_ep = get_adjacent_episodes(episode)
    col1, col2 = st.columns(2)

    with col1:
        if prev_ep:
            if st.button(
                f"← Previous: Ep {prev_ep['episode_number']}",
                key="prev_ep",
                use_container_width=True,
            ):
                st.session_state["selected_episode"] = prev_ep["slug"]
                st.rerun()

    with col2:
        if next_ep:
            if st.button(
                f"Next: Ep {next_ep['episode_number']} →",
                key="next_ep",
                use_container_width=True,
            ):
                st.session_state["selected_episode"] = next_ep["slug"]
                st.rerun()

    st.markdown("")

    # Next in this Arc
    related = get_related_episodes(episode)
    next_in_arc = None
    for rel in related:
        if rel.get("episode_number", 0) > ep_num:
            if next_in_arc is None or rel["episode_number"] < next_in_arc["episode_number"]:
                next_in_arc = rel

    if next_in_arc:
        if st.button(
            f"▶ Next in {arc}: Ep {next_in_arc['episode_number']} — {next_in_arc['title']}",
            key="next_in_arc",
            use_container_width=True,
        ):
            st.session_state["selected_episode"] = next_in_arc["slug"]
            st.rerun()

    # Explore full arc
    if st.button(
        f"Explore full arc: {arc} →",
        key="explore_arc",
        use_container_width=True,
    ):
        st.session_state["selected_episode"] = None
        st.session_state["filter_arc"] = arc
        st.rerun()

    st.markdown("")

    # More in this arc
    if related:
        st.markdown(f"### More in {arc}")
        for rel in related:
            rel_num = rel.get("episode_number", 0)
            rel_title = rel.get("title", "")
            rel_slug = rel.get("slug", "")
            if st.button(
                f"Ep {rel_num}: {rel_title}",
                key=f"related_{rel_slug}",
                use_container_width=True,
            ):
                st.session_state["selected_episode"] = rel_slug
                st.rerun()

    # Author footer
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    st.markdown(
        '<div style="font-size:13px;color:#999;padding:8px 0 32px 0;line-height:1.8;">'
        '<strong style="color:#777;">Vinod Alat</strong> &mdash; AI First Engineer | '
        'From Code to Context to Trust'
        '</div>',
        unsafe_allow_html=True,
    )
