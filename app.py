import streamlit as st
from utils.content_loader import (
    load_all_episodes,
    get_episode_by_slug,
    get_episodes_by_arc,
    get_featured_episodes,
    get_all_tags,
    ARCS,
)
from components.episode_card import render_episode_card, render_featured_card
from components.episode_detail import render_episode_detail

# --- Page Config ---
st.set_page_config(
    page_title="AI Podcast — The Shift in Software Engineering",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS (mobile-first) ---
st.markdown(
    """
    <style>
        /* Base — mobile first */
        .main .block-container {
            max-width: 1000px;
            padding-top: 1.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        h1 { font-weight: 800; color: #1a1a1a; font-size: 28px !important; }
        h2 { font-weight: 700; color: #2a2a2a; font-size: 22px !important; }
        h3 { font-weight: 600; color: #333; font-size: 18px !important; }

        /* Hide streamlit branding */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        /* Buttons — large touch targets, left-aligned text */
        .stButton > button {
            border: 1px solid #e0e0e0;
            background: #fafafa;
            color: #333;
            font-weight: 500;
            transition: all 0.2s;
            min-height: 44px;
            font-size: 14px;
            text-align: left !important;
            justify-content: flex-start !important;
            padding-left: 12px !important;
        }
        .stButton > button:hover {
            border-color: #333;
            background: #f0f0f0;
        }

        /* CTA buttons */
        .cta-primary > button {
            background: #E74C3C !important;
            color: white !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            min-height: 50px !important;
            text-align: center !important;
            justify-content: center !important;
            padding-left: 0 !important;
        }
        .cta-primary > button:hover {
            background: #C0392B !important;
        }
        .cta-secondary > button {
            background: white !important;
            color: #333 !important;
            border: 2px solid #333 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            min-height: 50px !important;
            text-align: center !important;
            justify-content: center !important;
            padding-left: 0 !important;
        }
        .cta-secondary > button:hover {
            background: #f5f5f5 !important;
        }

        /* Force Streamlit columns to stack on mobile */
        @media (max-width: 767px) {
            [data-testid="column"] {
                width: 100% !important;
                flex: 100% !important;
                min-width: 100% !important;
            }
            .stSelectbox, .stTextInput {
                margin-bottom: 8px;
            }
        }

        /* Desktop overrides */
        @media (min-width: 768px) {
            .main .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }
            h1 { font-size: 42px !important; }
            h2 { font-size: 28px !important; }
        }

        /* Video responsive */
        iframe {
            max-width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session State ---
if "selected_episode" not in st.session_state:
    st.session_state["selected_episode"] = None
if "filter_arc" not in st.session_state:
    st.session_state["filter_arc"] = "All"


def render_arc_quadrant(arc_name, arc_info, all_episodes):
    """Render a single arc quadrant card with episode buttons inline."""
    bg_colors = {
        "#E74C3C": "#fdf2f2",
        "#3498DB": "#f0f7fd",
        "#F39C12": "#fef9f0",
        "#2ECC71": "#f0fdf5",
    }
    color = arc_info["color"]
    bg = bg_colors.get(color, "#fafafa")
    arc_eps = [e for e in all_episodes if e.get("arc") == arc_name]
    arc_eps.sort(key=lambda e: e.get("episode_number", 999))

    # Arc header
    st.markdown(
        f'<div style="background:{bg};border:2px solid {color}22;border-top:4px solid {color};'
        f'border-radius:12px;padding:20px 20px 8px 20px;">'
        f'<div style="font-size:11px;color:{color};font-weight:700;text-transform:uppercase;'
        f'letter-spacing:1px;margin-bottom:4px;">Arc {arc_info["order"]}</div>'
        f'<div style="font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:6px;">{arc_name}</div>'
        f'<div style="font-size:13px;color:#777;margin-bottom:8px;line-height:1.4;">'
        f'{arc_info["description"]}</div></div>',
        unsafe_allow_html=True,
    )

    # Episode buttons (published) and labels (drafts)
    for ep in arc_eps:
        num = ep.get("episode_number", 0)
        title = ep.get("title", "")
        is_draft = ep.get("status") != "published"

        if is_draft:
            st.markdown(
                f'<div style="opacity:0.4;padding:4px 8px;font-size:13px;">'
                f'<span style="color:{color};font-weight:700;">Ep {num}</span> '
                f'{title} <span style="font-size:11px;color:#bbb;">(coming soon)</span></div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button(
                f"▶  Ep {num}: {title}",
                key=f"grid_{ep['slug']}",
                use_container_width=True,
            ):
                st.session_state["selected_episode"] = ep["slug"]
                st.rerun()


def render_arc_grid():
    """Render the 2x2 arc grid."""
    all_episodes = load_all_episodes(include_drafts=True)
    sorted_arcs = sorted(ARCS.items(), key=lambda x: x[1]["order"])

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        render_arc_quadrant(sorted_arcs[0][0], sorted_arcs[0][1], all_episodes)
    with col2:
        render_arc_quadrant(sorted_arcs[1][0], sorted_arcs[1][1], all_episodes)

    st.markdown("")

    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        render_arc_quadrant(sorted_arcs[2][0], sorted_arcs[2][1], all_episodes)
    with col4:
        render_arc_quadrant(sorted_arcs[3][0], sorted_arcs[3][1], all_episodes)


def render_footer():
    """Render About + Credits footer."""
    st.markdown("---")

    # About
    st.markdown(
        """
        <div style="padding:24px 0 16px 0;">
            <div style="font-size:18px;font-weight:700;color:#1a1a1a;margin-bottom:10px;">
                About This Series
            </div>
            <div style="font-size:14px;color:#555;line-height:1.7;max-width:700px;">
                <strong>Vinod Alat</strong> is an AI First Engineer working at the
                intersection of automotive software and AI-native development.
                <br><br>
                This series explores how software engineering is shifting from
                <strong>code</strong> to <strong>context</strong>,
                from <strong>context</strong> to <strong>trust</strong>,
                and from <strong>trust</strong> to <strong>systems</strong>.
                <br><br>
                <em>This is not a podcast about AI tools.
                This is a series about how AI changes engineering itself.</em>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Credits
    st.markdown(
        """
        <div style="padding:8px 0 32px 0;font-size:13px;color:#999;line-height:1.8;">
            <strong style="color:#777;">Credits</strong><br>
            Content &amp; narration: Vinod Alat<br>
            Video production: Google NotebookLM<br>
            Platform: Streamlit<br>
            Hosting: Streamlit Community Cloud
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_homepage():
    """Render the main landing page."""

    # --- Hero ---
    st.markdown(
        """
        <div style="text-align:center;padding:32px 8px 8px 8px;">
            <div style="font-size:13px;color:#999;font-weight:600;letter-spacing:1px;margin-bottom:16px;">
                Vinod Alat &mdash; AI First Engineer | From Code to Context to Trust
            </div>
            <div style="font-size:28px;font-weight:800;color:#1a1a1a;line-height:1.2;margin-bottom:12px;">
                AI is changing software engineering.<br>This series explains how.
            </div>
            <div style="font-size:15px;color:#555;max-width:650px;margin:0 auto;line-height:1.6;margin-bottom:8px;">
                A 15-part video series structured across 4 arcs:
                <strong>The Shift</strong> &rarr;
                <strong>The New Engineering Model</strong> &rarr;
                <strong>The Reality Check</strong> &rarr;
                <strong>The Future</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- CTA Buttons ---
    cta1, cta2 = st.columns(2)
    with cta1:
        st.markdown('<div class="cta-primary">', unsafe_allow_html=True)
        if st.button("Start with Episode 1", key="cta_start", use_container_width=True):
            st.session_state["selected_episode"] = "code-vs-trust"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cta2:
        st.markdown('<div class="cta-secondary">', unsafe_allow_html=True)
        if st.button("Explore by Arc", key="cta_explore", use_container_width=True):
            st.markdown('<script>document.getElementById("arc-grid").scrollIntoView()</script>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Positioning Line ---
    st.markdown(
        """
        <div style="text-align:center;padding:20px 8px 8px 8px;">
            <div style="font-size:14px;color:#888;font-style:italic;line-height:1.5;">
                This is not a podcast about AI tools.<br>
                This is a series about how AI changes engineering itself.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # --- Arc Grid ---
    st.markdown('<div id="arc-grid"></div>', unsafe_allow_html=True)
    render_arc_grid()

    st.markdown("")
    st.markdown("---")

    # --- Filter & Search ---
    st.markdown("## All Episodes")

    search = st.text_input("Search episodes", placeholder="Search by title or keyword...")

    col_arc, col_tag = st.columns(2)

    arc_options = ["All"] + [
        name for name, info in sorted(ARCS.items(), key=lambda x: x[1]["order"])
    ]
    with col_arc:
        selected_arc = st.selectbox(
            "Filter by Arc",
            arc_options,
            index=arc_options.index(st.session_state.get("filter_arc", "All")),
        )
        st.session_state["filter_arc"] = selected_arc

    all_tags = get_all_tags()
    with col_tag:
        selected_tag = st.selectbox("Filter by Tag", ["All"] + all_tags)

    st.markdown("")

    # --- Episode List ---
    episodes = load_all_episodes()

    if selected_arc != "All":
        episodes = [e for e in episodes if e.get("arc") == selected_arc]

    if selected_tag != "All":
        episodes = [e for e in episodes if selected_tag in e.get("tags", [])]

    if search:
        search_lower = search.lower()
        episodes = [
            e for e in episodes
            if search_lower in e.get("title", "").lower()
            or search_lower in e.get("summary", "").lower()
            or any(search_lower in tag.lower() for tag in e.get("tags", []))
        ]

    if not episodes:
        st.info("No episodes match your filters.")
    else:
        for episode in episodes:
            render_episode_card(episode)

    # --- Footer ---
    render_footer()


# --- Main Router ---
def main():
    selected_slug = st.session_state.get("selected_episode")

    if selected_slug:
        episode = get_episode_by_slug(selected_slug)
        if episode:
            render_episode_detail(episode)
        else:
            st.error("Episode not found.")
            if st.button("Back to Home"):
                st.session_state["selected_episode"] = None
                st.rerun()
    else:
        render_homepage()


if __name__ == "__main__":
    main()
