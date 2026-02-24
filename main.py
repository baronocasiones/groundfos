import streamlit as st
import pathlib

def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path('assets/styles.css')

st.title("3D Point Cloud **:blue[Upload]**", text_alignment="center")
st.caption("Upload your 3D point cloud files for AI-powered segmentation and rendering", text_alignment="center")

with st.container(border=True, gap="xxsmall", height="stretch"):
    st.subheader("Upload your File")
    st.caption("Select a 3D point cloud to begin")
    file = st.file_uploader("Click to upload",
                     label_visibility="hidden",
                     type=["ply", "pcd", "xyz", "txt"],
                     key='file-uploader',
                     )
    if file is not None:
        save_path = f"./files/{file.name}"
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"File saved to {save_path}")
