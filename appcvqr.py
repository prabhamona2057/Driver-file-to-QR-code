import streamlit as st
import qrcode
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="QR Drive Linker", layout="centered")

st.title("📂 Google Drive QR Generator & Scanner")

tab1, tab2 = st.tabs(["Generate QR Code", "Scan QR Code"])

# --- TAB 1: GENERATE ---
with tab1:
    st.header("Create QR Code")
    drive_url = st.text_input("Paste Google Drive Link:")
    
    if drive_url:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(drive_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_np = np.array(img.convert('RGB'))
        st.image(img_np, caption="Generated QR Code", use_container_width=True)
        
        st.download_button(
            label="Download QR Code",
            data=cv2.imencode('.png', img_np)[1].tobytes(),
            file_name="drive_qr.png",
            mime="image/png"
        )

# --- TAB 2: SCAN ---
with tab2:
    st.header("Scan QR Code")
    
    # Selection for scanning method
    scan_method = st.radio("Choose scan method:", ("Upload Image (Drag & Drop)", "Use Webcam"))
    
    scanned_image = None
    
    if scan_method == "Upload Image (Drag & Drop)":
        scanned_image = st.file_uploader("Drag and drop a QR code image here", type=['png', 'jpg', 'jpeg'])
    else:
        scanned_image = st.camera_input("Take a photo of the QR code")

    if scanned_image:
        # Convert the file to an opencv image
        file_bytes = np.asarray(bytearray(scanned_image.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        
        # QR Detection
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(opencv_img)
        
        if data:
            st.success("✨ QR Code Decoded!")
            st.info(f"Link: {data}")
            
            # Use a link button for cloud deployment compatibility
            st.link_button("🚀 Open Document", data)
        else:
            st.error("No QR code found in this image. Make sure it is clear and well-lit.")
