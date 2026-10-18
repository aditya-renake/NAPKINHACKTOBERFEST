"""
📸 Napkin2Code: Physical Sketch to Live Software
Hacktoberfest Hack Day Project
Turn hand-drawn paper sketches into working, interactive web applications in seconds
using 100% local, open-weight vision AI.
"""

import os
import io
import time
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

from core.image_processing import (
    enhance_sketch,
    image_to_bytes,
    load_image_from_bytes,
)
from engine.vision_ai import (
    check_ollama_status,
    generate_code_from_sketch,
    iterate_code_from_sketch,
    get_fallback_html,
    DEFAULT_VISION_MODELS,
)

# Page configuration
st.set_page_config(
    page_title="Napkin2Code — Physical Sketch to Live Software",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0f172a 100%);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-local {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-open {
        background-color: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }
    .badge-hack {
        background-color: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .action-btn-primary button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.4) !important;
    }
    .action-btn-primary button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.6) !important;
    }
    .action-btn-secondary button {
        background: linear-gradient(135deg, #e11d48 0%, #f43f5e 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 14px 0 rgba(225, 29, 72, 0.4) !important;
    }
    .action-btn-secondary button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(225, 29, 72, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "current_html" not in st.session_state:
    st.session_state.current_html = ""
if "iteration_history" not in st.session_state:
    st.session_state.iteration_history = []
if "last_action_meta" not in st.session_state:
    st.session_state.last_action_meta = None
if "selected_sample" not in st.session_state:
    st.session_state.selected_sample = None

# Top Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">
                📸 Napkin2Code <span style="font-size: 18px; font-weight: 400; color: #a5b4fc;">— Physical Sketch to Live Software</span>
            </h1>
            <p style="color: #cbd5e1; margin: 6px 0 0 0; font-size: 14px;">
                Hold real paper or a coffee napkin up to your webcam. Turn ink strokes into working, clickable Tailwind CSS apps via 100% local vision AI.
            </p>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <span class="badge-pill badge-local">🔒 100% Offline & Private</span>
            <span class="badge-pill badge-open">🧠 Open-Weight Vision</span>
            <span class="badge-pill badge-hack">🎃 Hacktoberfest Hack Day</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Local Vision AI Engine")

    # Ollama Connection Status
    ollama_status = check_ollama_status()
    if ollama_status["online"]:
        st.success(f"🟢 **Ollama Connected** (`localhost:11434`)")
        available_models = ollama_status.get("models", [])
        # Combine downloaded models with known supported models
        combined_models = list(dict.fromkeys(available_models + DEFAULT_VISION_MODELS))
        model_options = combined_models
    else:
        st.warning(f"🟡 **Ollama Offline** (Mock Demo Fallback Active)")
        model_options = DEFAULT_VISION_MODELS

    selected_model = st.selectbox(
        "Vision Model",
        options=model_options,
        index=0,
        help="Google Gemma 4 (E2B/E4B) provides frontier multimodal understanding. Moondream (1.86B) runs ultra-fast."
    )

    if any("gemma4" in m for m in ollama_status.get("models", [])):
        st.caption("✨ **Google Gemma 4 Vision Engine Active**")
    elif ollama_status["online"]:
        st.caption("💡 Tip: Pull Gemma 4 with `ollama pull gemma4:e2b` for state-of-the-art vision reasoning.")
    else:
        st.caption("💡 Run `ollama serve` and `ollama pull gemma4:e2b` in your terminal to enable live local AI.")

    st.divider()

    st.header("🎨 Ink Stroke Preprocessing")
    enable_enhancement = st.toggle("Ink Contrast Booster", value=True, help="Removes paper shadows and enhances ballpoint/marker contrast.")

    if enable_enhancement:
        contrast = st.slider("Contrast", min_value=1.0, max_value=2.8, value=1.8, step=0.1)
        sharpness = st.slider("Sharpness", min_value=1.0, max_value=3.5, value=2.0, step=0.1)
        brightness = st.slider("Paper Whitening", min_value=0.9, max_value=1.3, value=1.05, step=0.05)
    else:
        contrast = 1.0
        sharpness = 1.0
        brightness = 1.0

    st.divider()

    st.markdown("### 🏆 Hackathon Quicklinks")
    st.markdown("""
    - **Models**: [Gemma 4](https://ollama.com/library/gemma4) (Google) | [Moondream 2](https://github.com/vikhyat/moondream) | [Llama 3.2 Vision](https://ai.meta.com/llama/)
    - **Runtime**: [Ollama Local Server](https://ollama.com/)
    - **License**: Standard MIT Open Source
    """)

# Main Content: Split Screen
col_left, col_right = st.columns([1, 1], gap="large")

# ----------------- LEFT COLUMN: PHYSICAL INPUT -----------------
with col_left:
    st.subheader("📝 Step 1: Capture Paper Sketch")

    # Mode Selector: Initial vs Iteration
    mode = st.radio(
        "Select Workflow Mode:",
        options=["🚀 Initial Build (Paper -> New App)", "✏️ Physical Iterative Edit (Annotated Sketch -> Code Update)"],
        index=0 if not st.session_state.current_html else 1,
        help="Use 'Initial Build' for a new napkin sketch. Use 'Physical Iterative Edit' to upload a revised sketch with red pen scribbles or arrows to modify the live app."
    )

    is_iteration = "Physical Iterative Edit" in mode

    if is_iteration and not st.session_state.current_html:
        st.info("💡 You don't have an active app in memory yet. Generate an Initial Build first or load a sample sketch below!")

    # Input Method Tabs
    tab_webcam, tab_upload, tab_samples = st.tabs(["📷 Laptop Webcam", "📁 Upload Image", "🎯 Sample Sketches"])

    captured_image = None

    with tab_webcam:
        st.caption("Hold your paper sketch or napkin steadily up to your camera:")
        webcam_file = st.camera_input("Take a photo of your sketch", label_visibility="collapsed")
        if webcam_file is not None:
            captured_image = load_image_from_bytes(webcam_file.getvalue())

    with tab_upload:
        st.caption("Drop any photo of a sketch or whiteboard:")
        uploaded_file = st.file_uploader("Upload sketch", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
        if uploaded_file is not None:
            captured_image = load_image_from_bytes(uploaded_file.getvalue())

    with tab_samples:
        st.caption("Quickly test with realistic pre-drawn sketches without pen and paper:")
        sample_col1, sample_col2 = st.columns(2)
        with sample_col1:
            if st.button("🛒 Base Product Card Sketch", use_container_width=True):
                sample_path = "assets/samples/sample_product_card.png"
                if os.path.exists(sample_path):
                    st.session_state.selected_sample = sample_path
        with sample_col2:
            if st.button("✏️ Annotated Sketch (+ Red Pen)", use_container_width=True):
                sample_path = "assets/samples/sample_product_card_iterated.png"
                if os.path.exists(sample_path):
                    st.session_state.selected_sample = sample_path

        if st.session_state.selected_sample and os.path.exists(st.session_state.selected_sample):
            captured_image = Image.open(st.session_state.selected_sample).convert("RGB")
            st.caption(f"Loaded: `{os.path.basename(st.session_state.selected_sample)}`")

    # Image Preview & Enhancement
    if captured_image is not None:
        if enable_enhancement:
            processed_image = enhance_sketch(
                captured_image,
                contrast_factor=contrast,
                sharpness_factor=sharpness,
                brightness_factor=brightness,
            )
        else:
            processed_image = captured_image

        preview_expander = st.expander("🖼️ View Captured & Enhanced Sketch", expanded=True)
        with preview_expander:
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.caption("Raw Snapshot")
                st.image(captured_image, use_container_width=True)
            with p_col2:
                st.caption("Enhanced Ink Contrast")
                st.image(processed_image, use_container_width=True)

        user_guidance = st.text_input(
            "Optional guidance / extra notes (optional):",
            placeholder="e.g. 'Use modern dark mode', 'Make the cart button animate on click'",
        )

        # Action Buttons
        if not is_iteration:
            st.markdown('<div class="action-btn-primary">', unsafe_allow_html=True)
            if st.button("⚡ Compile Sketch to Interactive Web App", use_container_width=True):
                with st.spinner("🧠 Vision AI is analyzing strokes and generating Tailwind CSS..."):
                    result = generate_code_from_sketch(
                        image=processed_image,
                        model_name=selected_model,
                        user_guidance=user_guidance,
                    )
                    if result["success"]:
                        st.session_state.current_html = result["html"]
                        st.session_state.last_action_meta = result
                        st.session_state.iteration_history.append({
                            "type": "Initial Build",
                            "model": result["model"],
                            "elapsed": result["elapsed_seconds"],
                            "timestamp": time.strftime("%H:%M:%S"),
                            "mock": result.get("mock", False)
                        })
                        st.success(f"🎉 App compiled in {result['elapsed_seconds']}s via {result['model']}!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('error', 'Generation failed')}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="action-btn-secondary">', unsafe_allow_html=True)
            if st.button("✏️ Merge Physical Handwritten Edits into App", use_container_width=True):
                if not st.session_state.current_html:
                    st.error("Please generate an initial version first before applying iterative edits.")
                else:
                    with st.spinner("🔍 Reading pen scribbles and updating current code in real time..."):
                        result = iterate_code_from_sketch(
                            new_annotated_image=processed_image,
                            current_html=st.session_state.current_html,
                            user_notes=user_guidance,
                            model_name=selected_model,
                        )
                        if result["success"]:
                            st.session_state.current_html = result["html"]
                            st.session_state.last_action_meta = result
                            st.session_state.iteration_history.append({
                                "type": "Physical Revision",
                                "model": result["model"],
                                "elapsed": result["elapsed_seconds"],
                                "timestamp": time.strftime("%H:%M:%S"),
                                "mock": result.get("mock", False)
                            })
                            st.success(f"✨ Physical scribbles applied in {result['elapsed_seconds']}s!")
                            st.rerun()
                        else:
                            st.error(f"Error: {result.get('error', 'Iteration failed')}")
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------- RIGHT COLUMN: LIVE INTERACTIVE APP -----------------
with col_right:
    st.subheader("💻 Step 2: Live Interactive Application")

    if st.session_state.current_html:
        # Display Action Metadata banner
        meta = st.session_state.last_action_meta
        if meta:
            is_mock = meta.get("mock", False)
            badge_text = "🟡 Demo Fallback Mode" if is_mock else "🟢 100% Local Inference"
            st.caption(f"Status: **{badge_text}** | Engine: `{meta.get('model')}` | Latency: `{meta.get('elapsed_seconds')}s`")

        tab_preview, tab_code, tab_history, tab_export = st.tabs([
            "🌐 Live App (Interactive)",
            "📄 Source Code (HTML/Tailwind)",
            "⏱️ Iteration History",
            "📦 Export & Download"
        ])

        with tab_preview:
            # Render interactive iframe
            components.html(st.session_state.current_html, height=650, scrolling=True)

        with tab_code:
            st.code(st.session_state.current_html, language="html")

        with tab_history:
            st.markdown("#### 📜 Revision Log")
            for idx, item in enumerate(st.session_state.iteration_history, 1):
                icon = "🚀" if item["type"] == "Initial Build" else "✏️"
                mode_str = "(Demo Fallback)" if item.get("mock") else "(Local AI)"
                st.markdown(f"**{idx}. {icon} {item['type']}** — `{item['timestamp']}` | {item['elapsed']}s | `{item['model']}` {mode_str}")

        with tab_export:
            st.markdown("#### 📥 1-Click Code Export")
            st.markdown("Download your self-contained single-file HTML application. It requires zero build tools and can be opened in any browser or hosted on GitHub Pages.")
            st.download_button(
                label="⬇️ Download index.html",
                data=st.session_state.current_html,
                file_name="index.html",
                mime="text/html",
                use_container_width=True
            )
            if st.button("🗑️ Reset & Start New Napkin Sketch", use_container_width=True):
                st.session_state.current_html = ""
                st.session_state.iteration_history = []
                st.session_state.last_action_meta = None
                st.session_state.selected_sample = None
                st.rerun()
    else:
        # Placeholder empty state
        st.info("👈 Hold a sketch to your webcam or pick a sample on the left, then click 'Compile Sketch' to view the live interactive app here.")
        components.html(get_fallback_html("Awaiting physical sketch capture..."), height=650, scrolling=True)
