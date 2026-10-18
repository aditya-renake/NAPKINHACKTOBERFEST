"""Streamlit UI for Napkin2Code."""
import streamlit as st
import streamlit.components.v1 as components

import config
from core.image_processing import enhance
from engine.vision_ai import sketch_to_spec, extract_annotations
from engine.codegen import spec_to_html, edit_html

st.set_page_config(page_title="Napkin2Code", layout="wide", page_icon="📝")

st.title("📝 Napkin2Code")
st.caption("Turn a paper sketch into a live web app using 100% local open-weight AI. No cloud APIs, fully private.")

# Sidebar with model info and instructions
with st.sidebar:
    st.header("⚙️ Local AI Engine")
    st.markdown(f"**Vision Model:** `{config.VISION_MODEL}`")
    st.markdown(f"**Coder Model:** `{config.CODE_MODEL}`")
    st.markdown(f"**Max Image Side:** `{config.MAX_IMAGE_SIDE}px`")
    st.markdown("---")
    st.markdown("### 💡 Sketching Tips")
    st.markdown(
        "- Draw clear boxes for buttons, inputs, navigation, and cards.\n"
        "- Label elements clearly in legible print.\n"
        "- Use standard layouts (header, sidebar, content area).\n"
        "- To edit: use arrows, `+` notes, or cross out items."
    )
    st.markdown("---")
    st.caption("Make sure Ollama is running locally: `ollama run " + config.CODE_MODEL + "`")

if "html" not in st.session_state:
    st.session_state["html"] = ""
if "spec" not in st.session_state:
    st.session_state["spec"] = {}
if "last_error" not in st.session_state:
    st.session_state["last_error"] = ""

col_input, col_output = st.columns([1, 1], gap="medium")

with col_input:
    st.subheader("1. Input Sketch")
    input_mode = st.radio("Choose input method:", ["Camera", "Upload File"], horizontal=True)
    raw_image_bytes = None

    if input_mode == "Camera":
        cam_file = st.camera_input("Photograph your paper sketch")
        if cam_file:
            raw_image_bytes = cam_file.getvalue()
    else:
        uploaded_file = st.file_uploader("Upload an image of your sketch", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            raw_image_bytes = uploaded_file.getvalue()

    if raw_image_bytes:
        st.image(raw_image_bytes, caption="Input Preview", use_container_width=True)

        if st.button("🚀 Generate Web App", type="primary", use_container_width=True):
            st.session_state["last_error"] = ""
            with st.status("Generating web app from sketch...", expanded=True) as status:
                try:
                    st.write("1. Enhancing image contrast & sharpness...")
                    enhanced = enhance(raw_image_bytes)

                    st.write("2. Analyzing UI layout with vision model...")
                    spec = sketch_to_spec(enhanced)
                    st.session_state["spec"] = spec

                    st.write("3. Synthesizing HTML5 + Tailwind CSS...")
                    html = spec_to_html(spec)
                    st.session_state["html"] = html

                    status.update(label="App generated successfully!", state="complete")
                except Exception as err:
                    st.session_state["last_error"] = str(err)
                    status.update(label="Generation failed", state="error")

    if st.session_state["last_error"]:
        st.error(f"Error: {st.session_state['last_error']}")

    # Iteration section
    if st.session_state["html"]:
        st.markdown("---")
        st.subheader("2. Iterate & Edit")
        st.markdown("Refine your app by photographing annotated sketches or providing instructions:")

        iterate_mode = st.radio("Edit method:", ["Photograph Annotations", "Type Instruction"], horizontal=True)

        if iterate_mode == "Photograph Annotations":
            iter_file = st.file_uploader("Upload sketch with handwritten notes or arrows", type=["png", "jpg", "jpeg"], key="iter_upload")
            if iter_file and st.button("Apply Annotation Edits", use_container_width=True):
                with st.spinner("Extracting handwritten notes and updating code..."):
                    try:
                        enhanced_iter = enhance(iter_file.getvalue())
                        notes = extract_annotations(enhanced_iter)
                        if not notes:
                            st.warning("No new annotations detected in the image.")
                        else:
                            st.info(f"Detected instruction: {notes}")
                            updated_html = edit_html(st.session_state["html"], notes)
                            st.session_state["html"] = updated_html
                            st.rerun()
                    except Exception as err:
                        st.error(f"Failed to apply edit: {err}")
        else:
            text_instruction = st.text_input("Describe the change (e.g. 'Add a search bar at the top', 'Make button purple')")
            if st.button("Apply Text Edit", use_container_width=True) and text_instruction.strip():
                with st.spinner("Updating HTML..."):
                    try:
                        updated_html = edit_html(st.session_state["html"], text_instruction.strip())
                        st.session_state["html"] = updated_html
                        st.rerun()
                    except Exception as err:
                        st.error(f"Failed to apply edit: {err}")

with col_output:
    st.subheader("Output & Preview")

    if st.session_state["html"]:
        tab_preview, tab_code, tab_spec = st.tabs(["🖥️ Live Preview", "💻 HTML Code", "📋 UI Spec (JSON)"])

        with tab_preview:
            components.html(st.session_state["html"], height=650, scrolling=True)

        with tab_code:
            st.code(st.session_state["html"], language="html")

        with tab_spec:
            st.json(st.session_state.get("spec", {}))

        col_dl, col_reset = st.columns([2, 1])
        with col_dl:
            st.download_button(
                label="📥 Download HTML File",
                data=st.session_state["html"],
                file_name="index.html",
                mime="text/html",
                use_container_width=True,
            )
        with col_reset:
            if st.button("🗑️ Reset", use_container_width=True):
                st.session_state["html"] = ""
                st.session_state["spec"] = {}
                st.session_state["last_error"] = ""
                st.rerun()
    else:
        st.info("👋 Capture or upload a hand-drawn sketch on the left to see your live web app here!")
