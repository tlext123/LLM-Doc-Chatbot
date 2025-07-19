import streamlit as st
from rag_pipeline import answer_question_from_pdf, clean_text

st.title('PDF Analysis Chatbot')

pdf_file = st.file_uploader('Please submit a PDF for analysis', type=['pdf'])

question = st.text_input('What would you like to know?')


if st.button('Submit'):
    if pdf_file is not None and question:
        with open('temp_pdf', 'wb') as f:
            f.write(pdf_file.read())

        with st.spinner('Analyzing PDF'):
            answer = answer_question_from_pdf('temp_pdf', question)

        st.subheader('Answer')
        st.write(answer)

    else:
        st.warning('Please submit a valid PDF file and question')