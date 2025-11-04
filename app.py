import streamlit as st
from rag_pipeline import answer_question_from_pdf, clean_text



st.set_page_config(page_title="PDF Analysis Chatbot", layout='wide')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title('PDF Analysis Chatbot')

st.sidebar.header("Chat history")
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):
        st.sidebar.markdown(f"**you:** {chat['question']}")
        st.sidebar.markdown(f"**Bot:** {chat['answer']}")
        st.sidebar.markdown("---")

else:
    st.sidebar.info("No chat history. Ask a question.")

pdf_file = st.file_uploader('Please submit a PDF for analysis', type=['pdf'])

with st.form("question_form"):
    question = st.text_input('What would you like to know?')
    submitted = st.form_submit_button("Submit")


if submitted:
    if pdf_file is not None and question:
        with open('temp_pdf', 'wb') as f:
            f.write(pdf_file.read())

        with st.spinner('Analyzing PDF...'):
            answer = answer_question_from_pdf('temp_pdf', question)

        st.subheader('Answer')
        st.write(answer)

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer

        })

    else:
        st.warning('Please submit a valid PDF file and question')