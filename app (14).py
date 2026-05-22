import streamlit as st

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

    return response[0]['generated_text']

# ========================================
# CHAT DISPLAY
# ========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ========================================
# USER INPUT
# ========================================

user_input = st.chat_input("Ask about the medical report...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing report..."):

            ai_response = generate_response(user_input, report_text)

            st.markdown(ai_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

# ========================================
# DISCLAIMER
# ========================================

st.markdown("---")

st.warning(
    "⚠️ This AI-generated response is for educational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult a qualified doctor."
)
