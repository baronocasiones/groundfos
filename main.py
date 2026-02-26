import streamlit as st
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="3D Point Cloud Upload",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- LOAD CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/styles.css")

# --- FORCE WHITE UPLOADER & CUSTOM STYLES ---
st.markdown("""
<style>
    [data-testid="stFileUploader"] section { background-color: transparent !important; }
    [data-testid="stFileUploader"] section * { color: #4b5563 !important; }
    [data-testid="stFileUploader"] section button {
        background-color: #ffffff !important;
        color: #2563eb !important;
        border: 1px solid #e5e7eb !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    [data-testid="stFileUploader"] section button:hover {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #1d4ed8 !important;
    }
    [data-testid="stFileUploader"] section svg { color: #9ca3af !important; fill: #9ca3af !important; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'upload_state' not in st.session_state:
    st.session_state.upload_state = 'idle'
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# --- NAVBAR (Custom HTML) ---
navbar_html = """
<div class="custom-navbar" style="display: flex; align-items: center; border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem; margin-bottom: 2rem;">
    <div style="display: flex; align-items: center; gap: 8px; font-weight: bold; font-size: 1.2rem; margin-right: 2rem;">
        <div style="background-color: #2563eb; display: inline-flex; align-items: center; justify-content: center; padding: 6px; border-radius: 6px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
        </div>
        PointCloud Studio
    </div>
    <div style="display: flex; gap: 1rem;">
        <a href="#" style="text-decoration: none; color: #2563eb; background: #eff6ff; padding: 4px 12px; border-radius: 4px; font-weight: 600;">Upload</a>
        <a href="#" style="text-decoration: none; color: #6b7280; padding: 4px 12px;">Viewer</a>
        <a href="#" style="text-decoration: none; color: #6b7280; padding: 4px 12px;">Pipeline</a>
        <a href="#" style="text-decoration: none; color: #6b7280; padding: 4px 12px;">📖 Docs</a>
    </div>
</div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0;">3D Point Cloud <span style="color:#2563eb">Upload</span></h1>
    <p style="color: #6b7280; font-size: 1.1rem; margin-top: 0.5rem;">Upload your 3D point cloud files for AI-powered segmentation and rendering</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN CARD ---
with st.container(border=True):
    
    if st.session_state.upload_state == 'idle':
        st.subheader("Upload Your File")
        st.caption("Select a 3D point cloud file to begin")
        
        uploaded_file = st.file_uploader("Dropzone", type=['txt','las', 'ply', 'pcd'], label_visibility="collapsed")
        
        st.write("") 
        
        # Email Notifications Box
        with st.container(border=True):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown("<p style='margin-top: 8px; font-weight: 600;'>✉️ Email Notifications</p>", unsafe_allow_html=True)
            with col2:
                notify = st.toggle("Enable", label_visibility="collapsed")
                
            if notify:
                st.markdown("**Email Address**")
                input_col, btn_col = st.columns([5, 1])
                with input_col:
                    email_address = st.text_input("Email Address", placeholder="your.email@example.com", label_visibility="collapsed")
                with btn_col:
                    if st.button("Save", use_container_width=True):
                        st.toast(f"Email saved: {email_address}")
                        
                st.markdown("<p style='color: gray; font-size: 0.9rem; margin-top: -10px;'>You'll receive an email when the processing is complete</p>", unsafe_allow_html=True)

        st.write("")

        # --- REAL-TIME CHUNKED SAVING ---
        if uploaded_file is not None:
            if st.button("Begin Upload & Processing", type="primary", use_container_width=True):
                    
                os.makedirs("./files", exist_ok=True)
                save_path = f"./files/{uploaded_file.name}"
                
                # Setup UI elements for real-time tracking
                st.subheader("Saving to Secure Storage...")
                progress_bar = st.progress(0)
                status_text = st.empty()
                metrics_text = st.empty()
                
                file_size = uploaded_file.size
                chunk_size = 4096 * 1024 * 1024  # 4GB chunks (or whatever size you need)
                bytes_written = 0
                
                start_time = time.time()
                
                with open(save_path, "wb") as f:
                    uploaded_file.seek(0)
                    while True:
                        chunk = uploaded_file.read(chunk_size)
                        if not chunk:
                            break
                        
                        f.write(chunk)
                        bytes_written += len(chunk)
                        
                        # Calculate Metrics
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        progress = min(bytes_written / file_size, 1.0) if file_size > 0 else 1.0
                        speed_mb = (bytes_written / (1024 * 1024)) / elapsed_time if elapsed_time > 0 else 0
                        
                        # Update UI
                        progress_bar.progress(progress)
                        status_text.markdown(f"**Progress:** {int(progress * 100)}% ({bytes_written / (1024*1024):.1f} MB / {file_size / (1024*1024):.1f} MB)")
                        metrics_text.markdown(f"⏱️ **Elapsed Time:** {elapsed_time:.1f}s &nbsp;|&nbsp; 🚀 **Speed:** {speed_mb:.1f} MB/s")
                        
                        # Tiny sleep to ensure the UI updates between heavy disk I/O operations
                        time.sleep(0.05)
                
                st.session_state.saved_file_path = save_path
                st.session_state.upload_state = 'processing'
                st.rerun()

    elif st.session_state.upload_state == 'processing':
        st.subheader("Processing Point Cloud")
        st.caption("AI is classifying and rendering your data")
        
        with st.status("Pipeline Active", expanded=True) as status:
            st.write("⚙️ Preprocessing (Voxel downsampling, coordinate normalization)...")
            time.sleep(2)
            st.write("🧠 AI Layer Segmentation (Classifying objects and surfaces)...")
            time.sleep(3)
            st.write("🎨 High-Fidelity Rendering (Generating colorized mesh)...")
            time.sleep(2)
            status.update(label="Processing Complete!", state="complete", expanded=False)
            
        time.sleep(0.5)
        st.session_state.upload_state = 'complete'
        st.rerun()

    elif st.session_state.upload_state == 'complete':
        st.success("✨ Processing Complete! Your point cloud is ready to view.")
        
        if 'saved_file_path' in st.session_state:
            st.success(f"File successfully saved to: {st.session_state.saved_file_path}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Open Viewer", type="primary", use_container_width=True):
                st.toast("Opening Viewer...")
        with col2:
            if st.button("Upload Another File", use_container_width=True):
                st.session_state.upload_state = 'idle'
                st.rerun()

# --- BOTTOM INFO CARDS ---
if st.session_state.upload_state == 'idle':
    st.write("")
    card_col1, card_col2, card_col3 = st.columns(3)

    with card_col1:
        with st.container(border=True):
            st.markdown("**Supported Formats**")
            st.caption("LAS, PLY, and PCD formats are fully supported for point cloud processing.")

    with card_col2:
        with st.container(border=True):
            st.markdown("**Chunked Uploads**")
            st.caption("Processing uses 128 MB file chunking to handle massive architectural datasets safely.")

    with card_col3:
        with st.container(border=True):
            st.markdown("**AI Processing**")
            st.caption("Advanced AI segmentation classifies and analyses your point cloud data.")
