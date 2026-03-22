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
            max-width: 1100px;
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

        /* Buttons — large touch targets */
        .stButton > button {
            border: 1px solid #e0e0e0;
            background: #fafafa;
            color: #333;
            font-weight: 500;
            transition: all 0.2s;
            min-height: 44px;
            font-size: 14px;
        }
        .stButton > button:hover {
            border-color: #333;
            background: #f0f0f0;
        }

        /* Arc grid container */
        .arc-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }

        /* Arc quadrant card */
        .arc-quad {
            border-radius: 12px;
            padding: 20px;
            min-height: auto;
        }
        .arc-quad-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }
        .arc-quad-title {
            font-size: 18px;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 6px;
        }
        .arc-quad-desc {
            font-size: 13px;
            color: #777;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        .arc-ep-item {
            margin-bottom: 8px;
            padding: 6px 0;
        }
        .arc-ep-num {
            font-weight: 700;
            font-size: 14px;
        }
        .arc-ep-title {
            font-size: 14px;
            color: #333;
        }
        .arc-ep-draft {
            font-size: 11px;
            color: #bbb;
        }

        /* Hero section */
        .hero-section {
            text-align: center;
            padding: 24px 8px 16px 8px;
        }
        .hero-subtitle {
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        .hero-title {
            font-size: 28px;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 8px;
            line-height: 1.2;
        }
        .hero-desc {
            font-size: 15px;
            color: #555;
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* Episode card responsive */
        .ep-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            background: white;
        }

        /* Desktop overrides */
        @media (min-width: 768px) {
            .main .block-container {
                padding-left: 2rem;
                padding-right: 2rem;
            }
            h1 { font-size: 42px !important; }
            h2 { font-size: 28px !important; }
            .arc-grid {
                grid-template-columns: 1fr 1fr;
            }
            .arc-quad {
                padding: 24px;
                min-height: 220px;
            }
            .hero-section {
                padding: 40px 16px 20px 16px;
            }
            .hero-title {
                font-size: 42px;
            }
            .hero-desc {
                font-size: 18px;
            }
        }

        /* Force Streamlit columns to stack on mobile */
        @media (max-width: 767px) {
            [data-testid="column"] {
                width: 100% !important;
                flex: 100% !important;
                min-width: 100% !important;
            }
            /* Stack filter inputs vertically */
            .stSelectbox, .stTextInput {
                margin-bottom: 8px;
            }
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
    """Render a single arc quadrant card + buttons."""
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

    ep_items = ""
    for ep in arc_eps:
        num = ep.get("episode_number", 0)
        title = ep.get("title", "")
        is_draft = ep.get("status") != "published"
        opacity = "0.4" if is_draft else "1"
        draft_label = ' <span style="font-size:11px;color:#bbb;">(coming soon)</span>' if is_draft else ""
        ep_items += (
            f'<div style="opacity:{opacity};margin-bottom:8px;padding:4px 0;">'
            f'<span style="color:{color};font-weight:700;font-size:14px;">Ep {num}</span> '
            f'<span style="font-size:14px;color:#333;">{title}</span>'
            f'{draft_label}</div>'
        )

    st.markdown(
        f'<div style="background:{bg};border:2px solid {color}22;border-top:4px solid {color};'
        f'border-radius:12px;padding:20px;min-height:180px;">'
        f'<div style="font-size:11px;color:{color};font-weight:700;text-transform:uppercase;'
        f'letter-spacing:1px;margin-bottom:4px;">Arc {arc_info["order"]}</div>'
        f'<div style="font-size:18px;font-weight:800;color:#1a1a1a;margin-bottom:6px;">{arc_name}</div>'
        f'<div style="font-size:13px;color:#777;margin-bottom:12px;line-height:1.4;">'
        f'{arc_info["description"]}</div>'
        f'<div>{ep_items}</div></div>',
        unsafe_allow_html=True,
    )

    # Clickable buttons for published episodes
    pub_eps = [e for e in arc_eps if e.get("status") == "published"]
    if pub_eps:
        cols = st.columns(len(pub_eps))
        for idx, ep in enumerate(pub_eps):
            with cols[idx]:
                if st.button(
                    f"▶ Ep {ep['episode_number']}",
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


def render_homepage():
    """Render the main landing page."""
    # --- Hero ---
    st.markdown(
        """
        <div class="hero-section">
            <div style="font-size:13px;color:#999;font-weight:600;letter-spacing:1px;margin-bottom:6px;">
                Vinod Alat &mdash; AI First Engineer
            </div>
            <div class="hero-subtitle">AI Thought Leadership Series</div>
            <div class="hero-title">The Shift in Software Engineering</div>
            <div class="hero-desc">
                A 15-episode series exploring how software engineering is shifting
                from <strong>code</strong> to <strong>context</strong> to
                <strong>trust</strong> to <strong>systems</strong>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # --- Arc Grid ---
    render_arc_grid()

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
