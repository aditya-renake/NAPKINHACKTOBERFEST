"""Napkin2Code: Physical Sketch to Live Software.

Main Streamlit Application.
Hacktoberfest 'Best Open-Source AI Project' Submission.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from core.image_processor import enhance_sketch
from engine.vision_engine import (
    generate_code_from_sketch,
    check_ollama_status,
    SUPPORTED_MODELS,
    DEFAULT_OLLAMA_HOST,
)

# Page configuration
st.set_page_config(
    page_title="Napkin2Code | Physical Sketch to Live App",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #2563EB 0%, #7C3AED 50%, #DB2777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 1.2rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    .badge-green { background-color: #DEF7EC; color: #03543F; }
    .badge-amber { background-color: #FEF3C7; color: #92400E; }
    .badge-blue  { background-color: #E1EFFE; color: #1E429F; }
    </style>
""",
    unsafe_allow_html=True,
)

# Session State Initialization
if "current_html" not in st.session_state:
    st.session_state.current_html = ""
if "active_image" not in st.session_state:
    st.session_state.active_image = None
if "iteration_count" not in st.session_state:
    st.session_state.iteration_count = 0
if "last_status_msg" not in st.session_state:
    st.session_state.last_status_msg = ""
if "generation_log" not in st.session_state:
    st.session_state.generation_log = []

# Sidebar Controls
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/feathericons/feather/master/icons/camera.svg",
        width=40,
    )
    st.markdown("### ⚙️ System Settings")

    # Check Ollama daemon status
    is_ollama_up, available_models = check_ollama_status()
    if is_ollama_up:
        st.markdown(
            '<span class="badge badge-green">🟢 Ollama Connected</span>',
            unsafe_allow_html=True,
        )
        model_choices = available_models if available_models else SUPPORTED_MODELS
    else:
        st.markdown(
            '<span class="badge badge-amber">🟡 Offline Demo Mode</span>',
            unsafe_allow_html=True,
        )
        model_choices = SUPPORTED_MODELS

    selected_model = st.selectbox(
        "Vision Model",
        options=model_choices,
        index=0,
        help="Local open-weight vision model loaded in Ollama.",
    )

    st.markdown("---")
    st.markdown("### 🎨 Image Preprocessor")
    contrast_val = st.slider(
        "Ink Contrast Boost", 1.0, 3.0, 1.8, 0.1, help="Enhances pen lines on paper"
    )
    sharpness_val = st.slider(
        "Line Sharpness", 1.0, 3.0, 2.0, 0.1, help="Sharpens ink strokes"
    )
    auto_contrast_toggle = st.checkbox("Auto-level Background", value=True)

    st.markdown("---")
    st.markdown("### 🧪 Instant Demo Sketches")
    st.caption("Don't have paper ready? Test with these sample sketches:")

    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("📄 Sample Napkin", use_container_width=True):
            sample_path = "demo_assets/sample_napkin.png"
            if os.path.exists(sample_path):
                st.session_state.active_image = Image.open(sample_path)
                st.success("Loaded napkin sketch!")
    with col_demo2:
        if st.button("🖊️ Red-Pen Edit", use_container_width=True):
            annotated_path = "demo_assets/sample_annotated_napkin.png"
            if os.path.exists(annotated_path):
                st.session_state.active_image = Image.open(annotated_path)
                st.success("Loaded red-pen sketch!")

    st.markdown("---")
    if st.button("🔄 Reset Canvas & Code", use_container_width=True):
        st.session_state.current_html = ""
        st.session_state.active_image = None
        st.session_state.iteration_count = 0
        st.session_state.generation_log = []
        st.rerun()

    st.markdown("---")
    st.caption(
        "**Napkin2Code** • Open-Source License: MIT\n\nBuilt for Hacktoberfest Hack Day"
    )

# Main Header
st.markdown(
    '<div class="main-header">📸 Napkin2Code</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">Physical Paper Sketch to Live Software — Powered by Local Open-Weight Vision AI</div>',
    unsafe_allow_html=True,
)

# Status notification if any
if st.session_state.last_status_msg:
    st.info(st.session_state.last_status_msg)

# Layout: Split Screen
col_left, col_right = st.columns([1, 1], gap="large")

# LEFT COLUMN: CAMERA & PHYSICAL SKETCH INPUT
with col_left:
    st.markdown("### 📝 1. Capture Paper Sketch")

    input_mode = st.radio(
        "Input Source:",
        ["📸 Laptop Webcam", "📁 Upload Photo"],
        horizontal=True,
        label_visibility="collapsed",
    )

    raw_image = None
    if input_mode == "📸 Laptop Webcam":
        camera_snapshot = st.camera_input("Hold paper napkin/sketch up to camera")
        if camera_snapshot is not None:
            raw_image = Image.open(camera_snapshot)
            st.session_state.active_image = raw_image
    else:
        uploaded_file = st.file_uploader(
            "Upload image of paper sketch / whiteboard",
            type=["png", "jpg", "jpeg", "webp"],
        )
        if uploaded_file is not None:
            raw_image = Image.open(uploaded_file)
            st.session_state.active_image = raw_image

    # Display Active Image & Processed View
    if st.session_state.active_image is not None:
        processed_image = enhance_sketch(
            st.session_state.active_image,
            contrast=contrast_val,
            sharpness=sharpness_val,
            auto_contrast=auto_contrast_toggle,
        )

        st.image(
            processed_image,
            caption="Active Sketch (Ink Enhanced for Vision AI)",
            use_container_width=True,
        )

        # Action Buttons
        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            if st.button(
                "🚀 Generate Live App",
                type="primary",
                use_container_width=True,
                help="Generates brand new HTML/Tailwind app from sketch",
            ):
                with st.spinner("Analyzing sketch with local vision model..."):
                    html_code, live_used, msg = generate_code_from_sketch(
                        image=processed_image,
                        model=selected_model,
                        existing_html=None,
                    )
                    st.session_state.current_html = html_code
                    st.session_state.iteration_count = 1
                    st.session_state.last_status_msg = msg
                    st.session_state.generation_log.append(
                        "Iteration 1: Initial web app generated from physical sketch."
                    )
                    st.rerun()

        with btn_col2:
            is_disabled = len(st.session_state.current_html.strip()) == 0
            if st.button(
                "🖊️ Apply Red-Pen Edit",
                type="secondary",
                disabled=is_disabled,
                use_container_width=True,
                help="Updates existing app using your new handwritten annotations",
            ):
                with st.spinner("Merging physical annotations into code..."):
                    html_code, live_used, msg = generate_code_from_sketch(
                        image=processed_image,
                        model=selected_model,
                        existing_html=st.session_state.current_html,
                    )
                    st.session_state.current_html = html_code
                    st.session_state.iteration_count += 1
                    st.session_state.last_status_msg = msg
                    st.session_state.generation_log.append(
                        f"Iteration {st.session_state.iteration_count}: Physical red-pen annotations merged."
                    )
                    st.rerun()

    else:
        st.info(
            "👆 Snap a photo with your webcam or click **'📄 Sample Napkin'** in the sidebar to try it instantly!"
        )


# RIGHT COLUMN: INTERACTIVE LIVE PREVIEW & CODE
with col_right:
    st.markdown("### 🌐 2. Live Working Application")

    if st.session_state.current_html:
        tab_preview, tab_code, tab_log = st.tabs(
            ["🖥️ Interactive Preview", "💻 Generated HTML", "📜 Iteration Log"]
        )

        with tab_preview:
            # Render live interactive iframe with Tailwind CSS
            components.html(st.session_state.current_html, height=580, scrolling=True)

            col_down, col_refresh = st.columns([2, 1])
            with col_down:
                st.download_button(
                    label="⬇️ Download index.html",
                    data=st.session_state.current_html,
                    file_name="index.html",
                    mime="text/html",
                    use_container_width=True,
                )
            with col_refresh:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()

        with tab_code:
            st.code(st.session_state.current_html, language="html")

        with tab_log:
            st.markdown(f"**Total Iterations:** `{st.session_state.iteration_count}`")
            for log_entry in reversed(st.session_state.generation_log):
                st.markdown(f"- {log_entry}")

    else:
        # Placeholder view before generation
        st.markdown(
            """
            <div style="border: 2px dashed #CBD5E1; border-radius: 12px; padding: 4rem 2rem; text-align: center; color: #64748B;">
                <h4 style="color: #475569; margin-bottom: 0.5rem;">Your Live App Will Appear Here</h4>
                <p style="font-size: 0.9rem;">
                    1. Hold a paper sketch or napkin up to your webcam.<br>
                    2. Click <b>'Generate Live App'</b>.<br>
                    3. Draw red-pen changes on the paper and click <b>'Apply Red-Pen Edit'</b>!
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )
