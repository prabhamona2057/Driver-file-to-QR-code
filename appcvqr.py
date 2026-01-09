import streamlit as st
import qrcode
import cv2
import numpy as np
from PIL import Image
import webbrowser

st.set_page_config(page_title="QR Drive Linker", layout="centered")

st.title("📂 Google Drive QR Generator & Scanner")

tab1, tab2 = st.tabs(["Generate QR Code", "Scan QR Code"])

# --- TAB 1: GENERATE ---
with tab1:
    st.header("Create QR Code")
    drive_url = st.text_input("Paste Google Drive Link (Ensure 'Anyone with the link' is enabled):")
    
    if drive_url:
        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(drive_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to format Streamlit can display
        img_np = np.array(img.convert('RGB'))
        st.image(img_np, caption="Your Generated QR Code", use_container_width=True)
        
        # Download button
        st.download_button(
            label="Download QR Code",
            data=cv2.imencode('.png', img_np)[1].tobytes(),
            file_name="drive_qr.png",
            mime="image/png"
        )

# --- TAB 2: SCAN ---
with tab2:
    st.header("Scan QR Code via Webcam")
    
    # Use streamlit's camera input
    img_file = st.camera_input("Take a photo of the QR code")
    
    if img_file:
        # Convert the file to an opencv image
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        
        # Initialize the OpenCV QR code detector
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(opencv_img)
        
        if data:
            st.success(f"Found Link: {data}")
            if st.button("Open Document"):
                webbrowser.open(data)
        else:
            st.warning("No QR code detected. Please try again with better lighting.")
