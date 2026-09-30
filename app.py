import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered"
)

# -----------------------------
# App Header
# -----------------------------
st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.info(
    "LegalEase creates AI-generated document drafts. "
    "It is not a substitute for legal advice."
)

# -----------------------------
# Document Type
# -----------------------------
document_type = st.selectbox(
    "Select Document Type",
    [
        "Rental Agreement",
        "Leave/Application Letter",
        "General Notice",
        "Affidavit-style Draft",
        "NDA",
        "Employment Agreement"
    ]
)

# -----------------------------
# User Information
# -----------------------------
name = st.text_input("Name")

address = st.text_area("Address")

date = st.date_input("Date")

details = st.text_area(
    "Additional Details",
    placeholder="Enter the important details for the document..."
)

# -----------------------------
# Generate Document
# -----------------------------
if st.button("Generate Document"):

    # Get Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to your .env file."
        )
        st.stop()

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are an AI legal document drafting assistant.

Create a professional legal document DRAFT.

Document type:
{document_type}

Name:
{name}

Address:
{address}

Date:
{date}

Additional details:
{details}

Instructions:

1. Create a clear and professional legal document draft.
2. Use only the information provided by the user.
3. Do not invent important personal, financial, or legal facts.
4. Organize the document with clear headings and sections.
5. Include the provided date.
6. Clearly identify the person or party provided.
7. Use formal language appropriate for the selected document type.
8. Include relevant clauses based on the details provided.
9. Clearly state that this is an AI-generated draft.
10. State that the document should be reviewed by an appropriate
    legal professional before use.
11. Return only the document text.

This document is a draft and is not legal advice.
"""

    # -----------------------------
    # Call Gemini
    # -----------------------------
    try:

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        # -----------------------------
        # Display Generated Document
        # -----------------------------
        st.subheader("Generated Document")

        document_text = response.output_text

        st.text_area(
            "Document Draft",
            document_text,
            height=500
        )

        # -----------------------------
        # Download Button
        # -----------------------------
        file_name = (
            document_type
            .replace(" ", "_")
            .replace("/", "_")
            + ".txt"
        )

        st.download_button(
            label="Download Document",
            data=document_text,
            file_name=file_name,
            mime="text/plain"
        )

    except Exception as e:

        st.error(
            f"Error generating document: {e}"
        )