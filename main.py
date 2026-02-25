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
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Silently fail or add st.warning if you prefer

local_css("assets/styles.css")

# --- FORCE WHITE UPLOADER & CUSTOM STYLES ---
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
    
    /* Optional: Style the Save button to be dark gray */
    button[kind="secondaryFormSubmit"], button[kind="secondary"] {
        /* Add your dark gray button styles here if you want it to match perfectly */
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'upload_state' not in st.session_state:
    st.session_state.upload_state = 'idle'
if 'progress' not in st.session_state:
    st.session_state.progress = 0


# --- NAVBAR (Custom HTML) ---
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
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0;">3D Point Cloud <span style="color:#2563eb">Upload</span></h1>
    <p style="color: #6b7280; font-size: 1.1rem; margin-top: 0.5rem;">Upload your 3D point cloud files for AI-powered segmentation and rendering</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN CARD ---
with st.container(border=True):
    
    if st.session_state.upload_state == 'idle':
        # Card Headers
        st.subheader("Upload Your File")
        st.caption("Select a 3D point cloud file to begin")
        
        # Streamlit File Uploader
        uploaded_file = st.file_uploader("Dropzone", type=['las', 'ply', 'pcd'], label_visibility="collapsed")
        
        st.write("") # Spacer
        
        # Exact Email Notifications Box Layout
        with st.container(border=True):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown("<p style='margin-top: 8px; font-weight: 600;'>✉️ Email Notifications</p>", unsafe_allow_html=True)
            with col2:
                notify = st.toggle("Enable", label_visibility="collapsed")
                
            if notify:
                st.markdown("**Email Address**")
                
                # Align input and button side-by-side
                input_col, btn_col = st.columns([5, 1])
                with input_col:
                    email_address = st.text_input("Email Address", placeholder="your.email@example.com", label_visibility="collapsed")
                with btn_col:
                    if st.button("Save", use_container_width=True):
                        st.toast(f"Email saved: {email_address}")
                        
                st.markdown("<p style='color: gray; font-size: 0.9rem; margin-top: -10px;'>You'll receive an email when the processing is complete</p>", unsafe_allow_html=True)

        st.write("") # Spacer

        # Upload Action
        if uploaded_file is not None:
            if st.button("Begin Upload & Processing", type="primary", use_container_width=True):
                st.session_state.upload_state = 'uploading'
                st.rerun()

    elif st.session_state.upload_state == 'uploading':
        st.subheader("Uploading...")
        st.caption("Transferring file chunks to secure storage")
        
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
    st.write("") # Spacer
    card_col1, card_col2, card_col3 = st.columns(3)

    with card_col1:
        with st.container(border=True):
            st.markdown("**Supported Formats**")
            st.caption("LAS, PLY, and PCD formats are fully supported for point cloud processing.")

    with card_col2:
        with st.container(border=True):
            st.markdown("**Chunked Uploads**")
            st.caption("Large files are automatically split into chunks for reliable uploads.")

    with card_col3:
        with st.container(border=True):
            st.markdown("**AI Processing**")
            st.caption("Advanced AI segmentation classifies and analyses your point cloud data.")