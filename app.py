import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

# Website Page Configuration
st.set_page_config(page_title="PDF Unlocker Pro", page_icon="🔓", layout="centered")

st.title("🔓 PDF Password Remover")
st.info("Upload a locked PDF, enter the password, and download a permanent unlocked version.")

# 1. User Interface
uploaded_file = st.file_uploader("Upload your locked PDF", type="pdf")
password = st.text_input("Enter PDF Password", type="password", help="The current password of the file")

if uploaded_file and password:
    if st.button("Unlock PDF"):
        try:
            # Process in memory (Safe for web hosting)
            reader = PdfReader(uploaded_file)
            
            if reader.is_encrypted:
                # Attempt to decrypt
                decryption_result = reader.decrypt(password)
                
                if decryption_result == 0:
                    st.error("❌ Incorrect password. Please check and try again.")
                else:
                    # Create the unlocked version
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    # Convert to downloadable bytes
                    output_stream = io.BytesIO()
                    writer.write(output_stream)
                    unlocked_data = output_stream.getvalue()
                    
                    st.success("✅ PDF Unlocked! Ready for download.")
                    st.download_button(
                        label="📥 Download Unlocked PDF",
                        data=unlocked_data,
                        file_name=f"unlocked_{uploaded_file.name}",
                        mime="application/pdf"
                    )
            else:
                st.warning("This PDF is already unlocked.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
