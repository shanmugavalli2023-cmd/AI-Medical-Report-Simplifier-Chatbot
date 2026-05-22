import streamlit as st
from transformers import pipeline
import PyPDF2
import pdfplumber
import pytesseract
from PIL import Image

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Medical Report Simplifier",
    page_icon="🩺",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🩺 AI Medical Report Simplifier Chatbot")
st.write("Upload a medical report and ask AI questions.")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Upload Report")

uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

# ==========================================
# CHAT MEMORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():

    generator = pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )

    return generator

model = load_model()

# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_text_from_pdf(file):

    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(file)

        for page in pdf_reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    except:

        file.seek(0)

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

    return text

# ==========================================
# IMAGE OCR
# ==========================================

def extract_text_from_image(file):

    image = Image.open(file)

    text = pytesseract.image_to_string(image)

    return text

# ==========================================
# TXT EXTRACTION
# ==========================================

def extract_text_from_txt(file):

    return file.read().decode("utf-8")

# ==========================================
# PROCESS FILE
# ==========================================

report_text = ""

if uploaded_file is not None:

    file_type = uploaded_file.type

    with st.spinner("Extracting medical report text..."):

        if "pdf" in file_type:

            report_text = extract_text_from_pdf(uploaded_file)

        elif "image" in file_type:

            report_text = extract_text_from_image(uploaded_file)

        elif "text" in file_type:

            report_text = extract_text_from_txt(uploaded_file)

    st.success("Medical report processed successfully!")

# ==========================================
# DISPLAY REPORT
# ==========================================

if report_text:

    with st.expander("📄 Extracted Medical Report"):

        st.write(report_text)

# ==========================================
# AI RESPONSE FUNCTION
# ==========================================

def generate_response(user_question, medical_text):

    prompt = f"""
You are a helpful AI medical assistant.

Explain the following medical report in simple patient-friendly language.

Provide:
1. Disease explanation
2. Medicine explanation
3. Diet suggestions
4. Lifestyle advice
5. Emergency warning signs

Medical Report:
{medical_text}

User Question:
{user_question}
"""

    response = model(
        prompt,
        max_length=300,
        do_sample=True
    )

    return response[0]["generated_text"]

# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================

user_input = st.chat_input("Ask about the report...")

if user_input:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Analyzing report..."):

            ai_response = generate_response(
                user_input,
                report_text
            )

            st.markdown(ai_response)

    # Store AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

# ==========================================
# DISCLAIMER
# ==========================================

st.markdown("---")

st.warning(
    "⚠️ This AI-generated response is for educational purposes only and should not replace professional medical advice."
)
