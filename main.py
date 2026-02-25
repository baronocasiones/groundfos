import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="3D Point Cloud Upload",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- LOAD CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Ensure styles.css is in the same directory
try:
    local_css("assets/styles.css")
except FileNotFoundError:
    st.warning("styles.css not found. Please ensure it is in the same directory as main.py")

# --- FORCE WHITE UPLOADER ---
# This rigorously overrides Streamlit's dark theme dropzone to match the light UI
st.markdown("""
<style>
    /* Make the inner section transparent so it blends perfectly with our white dashed border */
    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }
    
    /* Force all text inside the dropzone to be dark gray */
    [data-testid="stFileUploader"] section * {
        color: #4b5563 !important;
    }

    /* Style the 'Browse files' button */
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

    /* Override the cloud icon color */
    [data-testid="stFileUploader"] section svg {
        color: #9ca3af !important;
        fill: #9ca3af !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'upload_state' not in st.session_state:
    st.session_state.upload_state = 'idle'
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# --- NAVBAR (Custom HTML matching image_3fd29e) ---
navbar_html = """
<div class="custom-navbar">
    <div class="nav-left">
        <div class="nav-title">
            <div class="nav-logo">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            </div>
            PointCloud Studio
        </div>
        <div class="nav-links">
            <a href="#" class="active">Upload</a>
            <a href="#">Viewer</a>
            <a href="#">Pipeline</a>
            <a href="#">Docs</a>
        </div>
    </div>
</div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">3D Point Cloud <span style="color:#2563eb">Upload</span></h1>
    <p class="hero-subtitle">Upload your 3D point cloud files for AI-powered segmentation and rendering</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN CARD ---
with st.container(border=True):
    
    if st.session_state.upload_state == 'idle':
        # Card Headers
        st.markdown('<p class="card-title">Upload Your File</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-desc">Select a 3D point cloud file to begin</p>', unsafe_allow_html=True)
        
        # Streamlit File Uploader
        uploaded_file = st.file_uploader("Dropzone", type=['las', 'ply', 'pcd'], label_visibility="collapsed")
        
        # Exact Email Notifications Box Layout
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown('''
            <div class="email-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                Email Notifications
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            notify = st.toggle("Enable", label_visibility="collapsed")
            
        if notify:
            email_address = st.text_input("Email Address", placeholder="your.email@example.com", label_visibility="collapsed")

        # Upload Action
        if uploaded_file is not None:
            if st.button("Begin Upload & Processing", type="primary", use_container_width=True):
                st.session_state.upload_state = 'uploading'
                st.rerun()

    elif st.session_state.upload_state == 'uploading':
        st.markdown('<p class="card-title">Uploading...</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-desc">Transferring file chunks to secure storage</p>', unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate Upload
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
            status_text.markdown(f"**Chunked Upload Progress:** {i+1}%")
            
        st.session_state.upload_state = 'processing'
        st.rerun()

    elif st.session_state.upload_state == 'processing':
        st.markdown('<p class="card-title">Processing Point Cloud</p>', unsafe_allow_html=True)
        st.markdown('<p class="card-desc">AI is classifying and rendering your data</p>', unsafe_allow_html=True)
        
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
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Open Viewer", type="primary", use_container_width=True):
                st.toast("Opening Viewer...")
        with col2:
            if st.button("Upload Another File", use_container_width=True):
                st.session_state.upload_state = 'idle'
                st.rerun()